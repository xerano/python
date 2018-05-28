# read temperature from fritz dect 200

import requests
import hashlib
import xml.etree.ElementTree as ET

username = "apiuser"
password = "123456"

session = requests.session()
resp = session.get("http://fritz.box/login_sid.lua")
tree = ET.fromstring(resp.text)

for child in tree:
    if child.tag == 'SID':
        sid = child.text
    if child.tag == 'Challenge':
        challenge = child.text


if challenge is None:
    print("Got no challenge from the box...")

md5 = hashlib.md5()
md5.update(bytes(challenge + "-" + password, 'utf-16le'))

auth_code = challenge+"-"+md5.hexdigest()

url = "http://fritz.box/login_sid.lua?username=%s&response=%s" % (username, auth_code)
print(url)

resp = requests.get(url)

tree = ET.fromstring(resp.text)

for child in tree:
    if child.tag == 'SID':
        sid = child.text
    if child.tag == 'Challenge':
        challenge = child.text

print(sid)

resp = requests.get("http://fritz.box/webservices/homeautoswitch.lua?sid="+sid+"&switchcmd=gettemperature&ain=087610199280")

print(int(resp.text) / 10.0)

session.close()