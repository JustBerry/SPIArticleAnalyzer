import requests
import getpass
import json

baseurl = 'https://en.wikipedia.beta.wmflabs.org/w/'
username = 'JustBerry'
password = getpass.getpass('Account password: ')
articlename = raw_input('Article to search: ')
# summary = 'bot hello'
# message = 'Hello Wikipedia. I am alive!'
# title = 'Sandbox'


# Requesting login
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(baseurl + 'api.php', data=payload)

# Confirming login
login_token = r1.json()['query']['tokens']['logintoken']
payload = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token}
r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

# Requesting all userids of users that have edited a particular page.
# Example/model: action=query&format=json&uselang=user&prop=revisions&titles=User%3AJustBerry&rvprop=user&rvlimit=max
payload = {
            'action': 'query',
            'format': 'json',
            'utf8': '',
            'uselang': 'user',
            'prop': 'revisions',
            'titles': articlename,
            'rvprop': 'contributors',
            'rvlimit': 'max'
          }

unparsed_getAllUsers = requests.get(baseurl + 'api.php', data=payload)
print unparsed_getAllUsers

# getAllUsers = json.loads(unparsed_getAllUsers)
# print getAllUsers

# Get editing token
# params3 = '?format=json&action=query&meta=tokens&continue='
# r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
# edit_token = r3.json()['query']['tokens']['csrftoken']
#
# edit_cookie = r2.cookies.copy()
# edit_cookie.update(r3.cookies)
#
# # Saving action
# payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message,'summary': summary, 'title': title, 'token': edit_token}
# r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)

# print (r4.text)
