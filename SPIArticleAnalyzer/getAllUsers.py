from __future__ import print_function, unicode_literals, with_statement

import requests
import json
import geoip2.database

from IPy import IP
from getAllUsersHelper import *

# Returns string output of report
def getAllUsers(article_name):

    baseurl = 'https://en.wikipedia.org/w/'

    # Requesting all users that have edited a particular page.

    requestParameters = {'action': 'query', 'format': 'json', 'prop': 'revisions', 'titles': article_name, 'rvlimit': 'max'}
    unparsed_allRevisions=requests.get(baseurl + 'api.php', params=requestParameters)
    revisionsDictionary = unparsed_allRevisions.json()
    if ('query' not in revisionsDictionary.keys()):
        return "Query: "  + unparsed_allRevisions.text
        # return "This page does not exist. Please try again."
    if ('pages' not in revisionsDictionary['query'].keys()):
        return "Pages: "  + unparsed_allRevisions.text
        # return "There are no pages for this query. Please try again."
    allPages = revisionsDictionary['query']['pages']
    allUsers = [];
    for page in allPages:
        for revision in unparsed_allRevisions.json()['query']['pages'][page]['revisions']:
            try:
                allUsers.append(revision['user'])
            except:
                pass

    # Removing duplicate (non-unique) users
    allUsers = list(set(allUsers))

    # From list of all users (allUsers) that have edited the specified article (article_name),
    # isolate a list of valid IP addresses (consisting of IPv4 and IPv6 addresses).

    allIPaddresses = []
    for user in allUsers:
        if (is_valid_ipv4_address(user) or is_valid_ipv6_address(user)):
            allIPaddresses.append(user)

    allUsers = list(set(allUsers) - set(allIPaddresses))

    # From the IP addresses list, separate out the IP addresses that
    # are private/internal (non-public) into a separate list.

    allInternalIPaddresses = []
    for address in allIPaddresses:
        if (IP(address).iptype()=='PRIVATE'):
            allInternalIPaddresses.append(address)

    allPublicIPaddresses = list(set(allIPaddresses) - set(allInternalIPaddresses))

    # Sort lists
    allUsers = sortNonIPList(allUsers)

    sortIPList(allPublicIPaddresses)

    sortIPList(allInternalIPaddresses)

    # Preparing output
    output = ""

    # Appending all registered users to output.
    if (allUsers is not None and len(allUsers)!=0):
        output += "All users:"
        for user in allUsers:
            output += "<br/>"
            output += "User:" + user
        output += "<br/><br/>"

    # Appending geolocation and all public IP addresses to output.
    if (len(allPublicIPaddresses)!=0):
        output += "All public IP addresses:"
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        for address in allPublicIPaddresses:
            response = reader.city(address)
            output += "<br/>"
            output += address + ' ('
            if (response.city.name is not None):
                output += response.city.name
                output += ', '
            if (response.subdivisions.most_specific.name is not None):
                output += response.subdivisions.most_specific.name
                output += ', '
            if (response.country.name is not None):
                output += response.country.name + ')'
        reader.close()
        output += "<br/><br/>"

    # Appending internal IP addresses
    if (len(allInternalIPaddresses)!=0):
        output += "All internal IP addresses:"
        for address in allInternalIPaddresses:
            output += "<br/>"
            output += address
        output += "<br/><br/>"

    return output
