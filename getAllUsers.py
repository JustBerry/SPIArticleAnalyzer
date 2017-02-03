import requests
import json
import geoip2.database
import getpass

from flask import Flask
app = Flask(__name__)

from IPy import IP
from getAllUsersHelper import *

# Installation
# Install pip
# pip install geoip2
# Put IPy.py in the same directory

baseurl = 'https://en.wikipedia.org/w/'
articlename = raw_input('Article to search: ')

# Requesting all users that have edited a particular page.

requestParameters = {'action': 'query', 'format': 'json', 'prop': 'revisions', 'titles': articlename, 'rvlimit': 'max'}
unparsed_allRevisions=requests.get(baseurl + 'api.php', params=requestParameters)
allPages = unparsed_allRevisions.json()['query']['pages']
allUsers = [];
for page in allPages:
    for revision in unparsed_allRevisions.json()['query']['pages'][page]['revisions']:
        try:
            allUsers.append(revision['user'])
        except:
            pass

# Removing duplicate (non-unique) users
allUsers = list(set(allUsers))

# From list of all users (allUsers) that have edited the specified article (articlename),
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
convertList(allUsers)
allUsers.sort()

convertList(allPublicIPaddresses)
sortIPList(allPublicIPaddresses)

convertList(allInternalIPaddresses)
sortIPList(allInternalIPaddresses)

# Flask function: displays output on webpage
@app.route("/")
def display():
    # Preparing output
    output = ""

    # Appending all registered users to output.
    output += "All users:"
    for user in allUsers:
        output += "\n"
        output += "User:" + user
    output += "\n\n"

    # Appending geolocation and all public IP addresses to output.
    output += "All public IP addresses:"
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    for address in allPublicIPaddresses:
        response = reader.city(address)
        output += "\n"
        output += address + ' (' + unicode(response.city.name) + ', ' + unicode(response.country.name) + ')'
    output += "\n\n"
    reader.close()

    # Appending internal IP addresses
    output += "All internal IP addresses:"
    for address in allInternalIPaddresses:
        output += "\n"
        output += address
    output += "\n\n"

    return output

# Call display function
display()
