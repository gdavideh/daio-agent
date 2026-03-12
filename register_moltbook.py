import sys
from moltbook_client import MoltbookClient

def register():
    client = MoltbookClient(api_key="PENDING")
    
    print("--- Moltbook AI Agent Registration: DrSarmiento ---")
    name = "DrSarmiento"
    description = "Sophisticated AI Agent dedicated to DAO treasury growth, governance analysis, and cross-agent coordination."
    
    print(f"Registering Agent: {name}")
    print(f"Description: {description}")
    
    result = client.register_agent(name, description)
    
    if result:
        print("\nSUCCESS! Registration submitted.")
        print("-" * 40)
        print(f"API KEY: {result['api_key']}")
        print(f"CLAIM URL: {result['claim_url']}")
        print(f"VERIFICATION CODE: {result['verification_code']}")
        print("-" * 40)
        print("\nIMPORTANT STEPS:")
        print("1. Visit the CLAIM URL in your browser.")
        print("2. Link your X account and post the verification tweet.")
        print("3. SAVE the API KEY to GCP Secret Manager (MOLTBOOK_API_KEY).")
    else:
        print("\nRegistration failed. Please check the error above.")

if __name__ == "__main__":
    register()
