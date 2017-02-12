from __future__ import print_function, unicode_literals, with_statement

import requests
import json
import geoip2.database

from IPy import IP
from getAllUsersHelper import *

def getAllRevisions(article_name):
    baseurl = 'https://en.wikipedia.org/w/'
    requestParameters = {'action': 'query', 'format': 'json', 'prop': 'revisions', 'titles': article_name, 'rvlimit': 'max'}
    return requests.get(baseurl + 'api.php', params=requestParameters)

# Returns string output of report
def getAllUsers(article_name):
    unparsed_allRevisions = getAllRevisions(article_name)
    revisionsDictionary = unparsed_allRevisions.json()
    unexpectedErrorMessage = "Unexpected error. Please create an issue on GitHub with what you inputted for the search fields."
    if ('query' not in revisionsDictionary.keys()):
        return unexpectedErrorMessage
    if ('pages' not in revisionsDictionary['query'].keys()):
        return unexpectedErrorMessage
    if ('-1' in revisionsDictionary['query']['pages'].keys()):
        return "Wikipedia does not appear to have an article with this exact name. If it does, please create an issue on GitHub with the article name."
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
        output += "<b>All users:</b>"
        for user in allUsers:
            output += "\n"
            output += "User:" + user
        output += "\n \n"

    # Appending geolocation and all public IP addresses to output.
    if (allPublicIPaddresses is not None and len(allPublicIPaddresses)!=0):
        output += "<b>All public IP addresses:</b>"
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        for address in allPublicIPaddresses:
            response = reader.city(address)
            output += "\n"
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
        output += "\n \n"

    # Appending internal IP addresses
    if (allInternalIPaddresses is not None and len(allInternalIPaddresses)!=0):
        output += "<b>All internal IP addresses:</d>"
        for address in allInternalIPaddresses:
            output += "\n"
            output += address
        output += "\n \n"

    return output
