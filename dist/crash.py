from urllib import request, parse
import json
import random
import time
import os

# if you wanna bomb the api, add "jared_" before it (e.g. "/blackjack/jared_data") please :)
base_url = "https://flask.puzzl3d.dev"
api = "/blackjack" # yeah ik im using the /blackjack api but i tried changing it to /casino and it kept breaking so stfu
data_endpoint = "/data"
top_endpoint = "/top"

username = None

class leaderboard:
    @staticmethod
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
    @staticmethod
    def get_top():
        try:
            with request.urlopen(f"{base_url}{api}{top_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            print("ERROR |",e)
            return {}
    @staticmethod
    def get_data():
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return {}
    @staticmethod
    def get_self_data():
        query_params = parse.urlencode({'name': username or leaderboard.get_user()})
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}?{query_params}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return {}
    @staticmethod
    def update(value):
        query_params = parse.urlencode({'name': username or leaderboard.get_user(), 'value': value, "roulette": True})
        req = request.Request(f"{base_url}{api}{data_endpoint}?{query_params}", method="POST")
        try:
            with request.urlopen(req) as response:
                charset = response.headers.get_content_charset()
                return response.read().decode(charset or 'utf-8')
        except Exception as e:
            return f"An error occurred: {e}"
    @staticmethod
    def ordinal_suffix(position):
        position = int(position)
        if 10 <= position % 100 <= 20:
            suffix = 'th'
        else:
            suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
            suffix = suffixes.get(position % 10, 'th')
        return f"{position}{suffix}"

cooldown = 60
user = leaderboard.get_user()


import math


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def getCrashChance(current_multiplier):
    return (-2**(-current_multiplier)) + 0.5

def get_top():
    data = leaderboard.get_top() or {}
    name = data.get("name", "Nobody")
    value = data.get("value", 0)
    if money > value:
        leaderboard.update(money)
        name = user
        value = money
    return name, value

def get_self_pos():
    data = leaderboard.get_data()
    sorted_data = sorted(data.keys(), key=lambda x: (-data[x].get("highest", 100), data[x].get("last_updated", 0)))
    try:
        position = sorted_data.index(user) + 1
        print(f"Your position in the leaderboard is {leaderboard.ordinal_suffix(position)} with ${data.get(user, {}).get('highest', 100)}!")
    except:
        print(f"You aren't on the leaderboard yet!")
        return None, sorted_data
    return position, sorted_data

def get_bet():
    name,value = get_top()
    print(f"{name} is top of the leaderboard with ${value}!")
    get_self_pos()
    print
    while True:
        try:
            bet = float(input(f"What's your bet (You have ${money})? "))
        except:
            print("Not a valid number")
        else:
            bet = round(bet*100)/100
            if bet > money:
                print("Not enough money")
            elif bet <= 0:
                print("Too low!")
            else:
                break
    clear_screen()
    return bet

def simulate_crash_game():
    current_multiplier = 1.0
    start_time = time.time()

    try:
        while True:
            elapsed = time.time() - start_time
            current_multiplier = math.pow(math.e, elapsed ** 2 / 20)  # Exponential growth, starting slow

            print(f"Current multiplier: {current_multiplier:.2f}x", end="\r")

            crash_chance = getCrashChance(current_multiplier)
            if random.randint(0, 1000)/1000 < crash_chance:
                print(f"\r\nCrashed at {current_multiplier:.2f}x!")
                return 0

            time.sleep(0.1)  # Update display every 0.1 seconds for smoother visuals

    except KeyboardInterrupt:
        # When the player decides to cash out
        print(f"\r\nCashed out at {current_multiplier:.2f}x")
        return current_multiplier

# Start the script
if __name__ == "__main__":
    data = leaderboard.get_self_data()
    money = data.get("current", 100)
    delta = time.time() - data.get("last_updated", 0)
    if money == 0 and delta > cooldown:
        money = 100
        leaderboard.update(money)
    elif money == 0:
        while True:
            clear_screen()
            delta = time.time() - data.get("last_updated", 0)
            if delta > cooldown: break
            else: print(f"You ran out of money! Play again in {round(cooldown-delta)} seconds")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)

    while True:
        while True:
            bet = get_bet()
            money -= bet
            multiplier = simulate_crash_game()
            money += bet * multiplier
            money = round(money * 100) / 100
            leaderboard.update(money)

            if money <= 0:
                break

        print(f"You ran out of money! Play again in {cooldown} seconds")
        start = time.time()
        time.sleep(1)
        while True:
            clear_screen()
            delta = time.time() - start
            if delta > cooldown: break
            else: print(f"{round(cooldown-delta)} seconds left!", end="")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)
