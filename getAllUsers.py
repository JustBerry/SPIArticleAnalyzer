import requests
import getpass
import json

baseurl = 'https://en.wikipedia.beta.wmflabs.org/w/'
# username = 'JustBerry'
# password = getpass.getpass('Account password: ')
articlename = raw_input('Article to search: ')
# summary = 'bot hello'
# message = 'Hello Wikipedia. I am alive!'
# title = 'Sandbox'

# Requesting all userids of users that have edited a particular page.

requestParameters = {'action': 'query', 'format': 'json', 'prop': 'revisions', 'titles': articlename, 'rvlimit': 'max'}
unparsed_allRevisions=requests.get(baseurl + 'api.php', params=requestParameters)
allRevisions = unparsed_allRevisions.json()['query']['pages']['1']['revisions']
allUsers = [];
i = 0;
for revision in allRevisions:
    allUsers.append(revision['user'])
    i+=1
print list(set(allUsers))[0:1]

# getAllUsers = json.loads(unparsed_getAllUsers)
# print getAllUsers

# 1. Requesting login
# payload = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'login'}
# r1 = requests.post(baseurl + 'api.php', data=payload)

# 2. Confirming login
# login_token = r1.json()['query']['tokens']['logintoken']
# payload = {'action': 'login', 'format': 'json', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token}
# r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

# 3. Get editing token
# params3 = '?format=json&action=query&meta=tokens&continue='
# r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
# edit_token = r3.json()['query']['tokens']['csrftoken']

# edit_cookie = r2.cookies.copy()
# edit_cookie.update(r3.cookies)

# 4. Saving action
# payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'appendtext': message,'summary': summary, 'title': title, 'token': edit_token}
# r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)

# 5. Final output
# print (r4.text)
