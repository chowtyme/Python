import requests
import json

ZENDESK_DOMAIN = "orgdomainzendesk"
ZENDESK_EMAIL = "youremailaddress"
ZENDESK_API_TOKEN = "rawr1337"

TERMINATED_USERS = [
        "eazyenough@site.com"
]

def offboard_users():
    zendesk_auth = (ZENDESK_EMAIL + "/token", ZENDESK_API_TOKEN)
    headers = {"Content-Type": "application/json"}

    for user_email in TERMINATED_USERS:
        search_url = f"https://{ZENDESK_DOMAIN}/api/v2/search.json?query=type:user {user_email}"
        response = requests.get(search_url, auth=zendesk_auth, headers=headers)
        user_data = response.json()

        if user_data["count"] > 0:
            user_id = user_data["results"][0]["id"]
            user_name = user_data["results"][0]["name"]

            update_url = f"https://{ZENDESK_DOMAIN}/api/v2/users/{user_id}.json"
            update_data = {
                "user": {
                    "id": user_id,
                    "role": "end-user",
                    "suspended": True
                }
            }
            response = requests.put(update_url, auth=zendesk_auth, headers=headers, data=json.dumps(update_data))

            if response.status_code == 200:
                print(f"Offboarded user: {user_name} ({user_email})")
            else:
                print(f"Error offboarding user: {user_name} ({user_email})")

if __name__ == "__main__":
    offboard_users()