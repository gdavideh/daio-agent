from google.cloud import secretmanager
import os

class SecurityManager:
    def __init__(self, project_id="daio-agent"):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id, version_id="latest"):
        """
        Accesses a secret version in GCP Secret Manager.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def load_all_secrets(self):
        """
        Loads all required secrets into the environment for legacy compatibility 
        or returns them as a dictionary.
        """
        secrets = {
            "GEMINI_API_KEY": self.get_secret("GEMINI_API_KEY"),
            "AGENT_PRIVATE_KEY": self.get_secret("AGENT_PRIVATE_KEY"),
            "MOLTBOOK_API_KEY": self.get_secret("MOLTBOOK_API_KEY"),
            "CLAUDE_API_KEY": self.get_secret("CLAUDE_API_KEY")
        }
        return secrets

if __name__ == "__main__":
    # Test (requires GCP ADC or running on GCP VM)
    try:
        sm = SecurityManager()
        # print(f"Successfully fetched Gemini Key: {sm.get_secret('GEMINI_API_KEY')[:5]}...")
    except Exception as e:
        print(f"Could not fetch secrets: {e}. Ensure you are authenticated with gcloud.")
