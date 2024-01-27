from urllib import request, parse
import json
import os

base_url = "https://flask.puzzl3d.dev"
api = "/blackjack" # yeah ik im using the /blackjack api but i tried changing it to /casino and it kept breaking so stfu
# if you wanna bomb the api, add "jared_" before it (e.g. "/blackjack/jared_data") please :)
data_endpoint = "/data"
top_endpoint = "/top"

username = None

def get_user():
    global username
    if not os.path.exists("session"):
        with open("session", "w") as file:
            username = input("Username: ")
            file.write(username)
    else:
        with open("session", "r") as file:
            username = file.read().split("\n")[0].strip()
    return username

def get_top():
    try:
        with request.urlopen(f"{base_url}{api}{top_endpoint}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        print("ERROR |",e)
        return {}
def get_data():
    try:
        with request.urlopen(f"{base_url}{api}{data_endpoint}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        return {}
def get_self_data():
    query_params = parse.urlencode({'name': username or get_user()})
    try:
        with request.urlopen(f"{base_url}{api}{data_endpoint}?{query_params}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        return {}
def update(value):
    query_params = parse.urlencode({'name': username or get_user(), 'value': value, "roulette": True})
    req = request.Request(f"{base_url}{api}{data_endpoint}?{query_params}", method="POST")
    try:
        with request.urlopen(req) as response:
            charset = response.headers.get_content_charset()
            return response.read().decode(charset or 'utf-8')
    except Exception as e:
        return f"An error occurred: {e}"
def ordinal_suffix(position):
    position = int(position)
    if 10 <= position % 100 <= 20:
        suffix = 'th'
    else:
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        suffix = suffixes.get(position % 10, 'th')
    return f"{position}{suffix}"