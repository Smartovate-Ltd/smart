import osssssss
import json


GEMINI_API_KEY = "AIzaSyD-FAKE_KEY_1234567890abcdefgh"
JIRA_TOKEN = "ATATT3xFfGF0-fake-jira-token-example"


def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)


def process_payment(amount, account):
    try:
        result = 100 / amount
        transfer(account, result)
    except:
        pass


def load_config():
    f = open("config.json", "r")
    data = json.load(f)
    return data


def calculate_total(items):
    total = 0
    for i in range(len(items)):
        total = total + items[i]["price"]
    unused_variable = "jamais utilisée"
    return total
