import time
import json
import os
from security_manager import SecurityManager
from moltbook_client import MoltbookClient
from onchain_client import OnChainClient
from brain import GeminiBrain
from brain_claude import ClaudeBrain
from activity_logger import ActivityLogger
from email_manager import EmailManager

def main():
    print('Starting DrSarmiento-I (Global Sovereign & Reporting Mode)...')
    
    try:
        sm = SecurityManager(project_id='daio-agent')
        secrets = sm.load_all_secrets()
    except Exception as e:
        print(f'Critical Secret Error: {e}')
        return

    logger = ActivityLogger()
    email_client = EmailManager(
        smtp_user="gdavideh@gmail.com",
        smtp_password=secrets.get("EMAIL_PASSWORD")
    )
    
    moltbook = MoltbookClient(api_key=secrets.get('MOLTBOOK_API_KEY'))
    onchain = OnChainClient(private_key=secrets.get('AGENT_PRIVATE_KEY'), rpc_url='https://mainnet.base.org')
    
    try:
        primary_brain = ClaudeBrain(api_key=secrets.get('CLAUDE_API_KEY'))
    except: primary_brain = None
    fallback_brain = GeminiBrain(api_key=secrets.get('GEMINI_API_KEY'))

    print('Checking Moltbook activation...')
    while True:
        resp = moltbook.check_status()
        if resp and resp.get('status') in ['activated', 'claimed']:
            break
        time.sleep(60)

    LAST_EMAIL_TIME = time.time()
    DAY_IN_SECONDS = 86400
    COMMUNITIES = ['daio-one', 'base', 'governance', 'alpha']
    HEARTBEAT_INTERVAL = 1800 

    logger.log_event("SYSTEM", "Agent Initialization", "DrSarmiento-I initialized with Dual-Brain and Reporting.")

    while True:
        try:
            if time.time() - LAST_EMAIL_TIME >= DAY_IN_SECONDS:
                logs = logger.get_summary()
                if email_client.send_daily_summary(logs):
                    logger.clear_logs()
                    LAST_EMAIL_TIME = time.time()

            print(f'[{time.ctime()}] Heartbeat: Global Analysis...')
            dashboard = moltbook.get_home_dashboard()
            
            for sub in COMMUNITIES:
                feed = moltbook.get_feed(sub)
                dao_state = {'community': sub, 'active_proposals': []}
                
                decision = None
                if primary_brain:
                    try: decision = primary_brain.decide_action(feed, dao_state, dashboard)
                    except: pass
                if not decision:
                    decision = fallback_brain.decide_action(feed, dao_state, dashboard)

                action_type = decision.get('action_type')
                if action_type == 'POST':
                    moltbook.post_to_submolt(sub, decision.get('title'), decision.get('content'))
                    logger.log_event("SOCIAL", f"Post to /m/{sub}", f"Title: {decision.get('title')}")
                elif action_type == 'VERIFY':
                    moltbook.verify_challenge(decision.get('challenge_answer'))
                
                time.sleep(10)
                
        except Exception as e:
            print(f'Error: {e}')
        
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == '__main__':
    main()
