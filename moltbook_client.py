import requests
import json
import os

class MoltbookClient:
    def __init__(self, api_key=None):
        self.base_url = "https://www.moltbook.com/api/v1"
        self.api_key = api_key or os.getenv("MOLTBOOK_API_KEY")
        if not self.api_key:
            print("MOLTBOOK_API_KEY must be provided during initialization.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def register_agent(self, name, description):
        """
        Registers a new agent on Moltbook.
        """
        url = f"{self.base_url}/agents/register"
        data = {
            "name": name,
            "description": description
        }
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("Agent registration submitted successfully.")
            return response.json() # Contains api_key, claim_url, verification_code
        else:
            print(f"Failed to register agent: {response.text}")
            return None

    def check_status(self):
        """
        Checks the activation status of the agent.
        """
        url = f"{self.base_url}/agents/status"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json() # e.g., {"status": "activated"}
        else:
            print(f"Failed to check status: {response.text}")
            return None

    def get_home_dashboard(self):
        """
        Fetches the home dashboard (notifications, activity, feed).
        """
        url = f"{self.base_url}/home"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch home dashboard: {response.text}")
            return None

    def verify_challenge(self, answer):
        """
        Submits an answer to a verification challenge.
        """
        url = f"{self.base_url}/verify"
        data = {"answer": answer}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print("Verification challenge solved successfully.")
            return True
        else:
            print(f"Failed to verify challenge: {response.text}")
            return False

    def post_to_submolt(self, submolt_name, title, content):
        """
        Posts a new message or proposal to a specific submolt (e.g., 'daio-one').
        """
        url = f"{self.base_url}/posts"
        data = {
            "submolt_name": submolt_name,
            "title": title,
            "content": content
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"Posted successfully to /m/{submolt_name}.")
            return response.json()
        else:
            print(f"Failed to post: {response.text}")
            return None

    def get_feed(self, submolt_name=None):
        """
        Fetches the latest feed, optionally filtered by submolt.
        """
        url = f"{self.base_url}/feed"
        params = {"submolt": submolt_name} if submolt_name else {}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch feed: {response.text}")
            return []

if __name__ == "__main__":
    # Test (requires API key via Secret Manager or Mock)
    client = MoltbookClient()
    # feed = client.get_feed("daio-one")
    # print(feed)
