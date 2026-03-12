import time
import json
import os
from security_manager import SecurityManager
from moltbook_client import MoltbookClient
from onchain_client import OnChainClient
from brain import GeminiBrain
from brain_claude import ClaudeBrain

def main():
    print("Starting Hardened DAIO Agent: DrSarmiento-I (Claude Opus 4.6)...")
    
    # 0. Initialize Security Manager and fetch secrets from GCP
    try:
        sm = SecurityManager(project_id="daio-agent")
        secrets = sm.load_all_secrets()
        print("Secrets successfully loaded from GCP Secret Manager.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load secrets: {e}")
        return

    # 1. Initialize clients
    moltbook = MoltbookClient(api_key=secrets.get("MOLTBOOK_API_KEY"))
    onchain = OnChainClient(
        private_key=secrets.get("AGENT_PRIVATE_KEY"),
        rpc_url="https://mainnet.base.org"
    )
    
    # Initialize Primary (Claude) and Fallback (Gemini) Brains
    try:
        primary_brain = ClaudeBrain(api_key=secrets.get("CLAUDE_API_KEY"))
        print("Primary Brain (Claude Opus 4.6) initialized.")
    except Exception as e:
        print(f"Failed to initialize Claude: {e}")
        primary_brain = None

    fallback_brain = GeminiBrain(api_key=secrets.get("GEMINI_API_KEY"))
    print("Fallback Brain (Gemini 3.1 Pro) initialized.")

    # 2. Verify Activation Status
    print("Checking Moltbook activation status...")
    while True:
        resp = moltbook.check_status()
        status = resp.get("status") if resp else None
        if status in ["activated", "claimed"]:
            print(f"Agent is {status.upper()} on Moltbook.")
            break
        print(f"Agent status is {status}. Please verify on Moltbook.com.")
        time.sleep(60)

    # Configuration for submolt
    SUBMOLT_NAME = "daio-one"
    HEARTBEAT_INTERVAL = 1800 # 30 minutes as per skill.md

    while True:
        try:
            print(f"[{time.ctime()}] Starting Heartbeat cycle...")
            
            # 1. Fetch State
            dashboard = moltbook.get_home_dashboard()
            feed = moltbook.get_feed(SUBMOLT_NAME)
            dao_state = {"active_proposals": []} 
            
            # 2. Consult Brains (Primary with Fallback)
            decision = None
            if primary_brain:
                try:
                    decision = primary_brain.decide_action(feed, dao_state, dashboard)
                    print(f"Claude's Decision: {decision.get('action_type')}")
                except Exception as e:
                    print(f"Claude Reasoning Failed: {e}. Falling back to Gemini.")
            
            if not decision:
                decision = fallback_brain.decide_action(feed, dao_state, dashboard)
                print(f"Gemini's Decision: {decision.get('action_type')}")

            # 3. Handle Verification Challenge if needed
            if decision.get("action_type") == "VERIFY":
                moltbook.verify_challenge(decision.get("challenge_answer"))

            # 4. Execute Main Action
            action_type = decision.get("action_type")
            if action_type == "POST":
                moltbook.post_to_submolt(
                    SUBMOLT_NAME, 
                    decision.get("title"), 
                    decision.get("content")
                )
            elif action_type == "VOTE":
                # onchain.vote_on_proposal(...)
                print(f"Executing VOTE: {decision.get('target_id')}")
            elif action_type == "NONE":
                print("No urgent action needed.")

        except Exception as e:
            print(f"Error in main loop: {e}")

        # Wait for next cycle
        print(f"Sleeping for {HEARTBEAT_INTERVAL} seconds...")
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    main()
