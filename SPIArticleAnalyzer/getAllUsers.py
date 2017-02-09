from __future__ import print_function, unicode_literals, with_statement

import requests
import json
import geoip2.database
import getpass

from IPy import IP
from getAllUsersHelper import *

import matplotlib

import argparse
import contextlib
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Installation
# Install pip
# pip install geoip2
# Put IPy.py in the same directory

# def get_lat_lon(ip_list=[], lats=[], lons=[]):
#     """
#     This function connects to the FreeGeoIP web service to get info from
#     a list of IP addresses.
#     Returns two lists (latitude and longitude).
#     """
#     print("Processing {} IPs...".format(len(ip_list)))
#     for ip in ip_list:
#         r = requests.get("https://freegeoip.net/json/" + ip)
#         json_response = r.json()
#         print("{ip}, {region_name}, {country_name}, {latitude}, {longitude}".format(**json_response))
#         if json_response['latitude'] and json_response['longitude']:
#             lats.append(json_response['latitude'])
#             lons.append(json_response['longitude'])
#     return lats, lons

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
    sortNonIPList(allUsers)

    sortIPList(allPublicIPaddresses)

    sortIPList(allInternalIPaddresses)

    # Preparing output
    output = ""

    # Appending all registered users to output.
    if (len(allUsers)!=0):
        output += "All users:"
    for user in allUsers:
        output += "<br/>"
        output += "User:" + user
    if (len(allUsers)!=0):
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
    if (len(allPublicIPaddresses)!=0):
        output += "<br/><br/>"

    # Appending internal IP addresses
    if (len(allInternalIPaddresses)!=0):
        output += "All internal IP addresses:"
    for address in allInternalIPaddresses:
        output += "<br/>"
        output += address
    if (len(allInternalIPaddresses)!=0):
        output += "<br/><br/>"

    print ("All public IPs: ")
    print (allPublicIPaddresses)
    lats = []
    lons = []
    cannotGeolocateIPaddresses = []
    wesn = None
    for address in allPublicIPaddresses:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(address)
        if (response.location.latitude is not None and response.location.longitude is not None):
            lats.append(response.location.latitude)
            lons.append(response.location.longitude)
        else:
            cannotGeolocateIPaddresses.append(address)

    print ("Lats before: ")
    print (lats)
    print ("Lons before: ")
    print (lons)
    print (cannotGeolocateIPaddresses)
    # get_lat_lon(cannotGeolocateIPaddresses, lats, lons)
    # print ("Lats after: ")
    # print (lats)
    # print ("Lons after: ")
    # print (lons)

    output = 'image.png'
    # def generate_map(output, lats=[], lons=[], wesn=None):
    """
    Using Basemap and the matplotlib toolkit, this function generates a map and
    puts a red dot at the location of every IP addresses found in the list.
    The map is then saved in the file specified in `output`.
    """
    print("Generating map and saving it to {}".format(output))
    if wesn:
        wesn = [float(i) for i in wesn.split('/')]
        m = Basemap(projection='cyl', resolution='l',
                llcrnrlon=wesn[0], llcrnrlat=wesn[2],
                urcrnrlon=wesn[1], urcrnrlat=wesn[3])
    else:
        m = Basemap(projection='cyl', resolution='l')
    m.bluemarble()
    x, y = m(lons, lats)
    m.scatter(x, y, s=1, color='#ff0000', marker='o', alpha=0.3)
    plt.savefig(output, dpi=600, bbox_inches='tight')

    output += '<img src="image.png">'
    return output
