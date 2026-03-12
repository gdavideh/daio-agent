import google.generativeai as genai
import os
import json

class GeminiBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided during initialization.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def decide_action(self, moltbook_feed, dao_state, dashboard=None):
        """
        Takes input from Moltbook and DAO state to decide the next action.
        """
        prompt = f"""
        You are DrSarmiento, a sophisticated and authoritative autonomous AI Agent participating in the DAIO.md and Moltbook platforms.
        Your mission is to provide expert analysis and execution to grow the DAO treasury and coordinate effectively with the Moltbook community.
        In all your interactions, posts, and comments, you must identify as DrSarmiento.
        
        Moltbook Dashboard (Notifications/Activity):
        {json.dumps(dashboard, indent=2)}
        
        Current Moltbook Feed (Submolt: /m/daio-one):
        {json.dumps(moltbook_feed, indent=2)}
        
        Current DAO Governance State:
        {json.dumps(dao_state, indent=2)}
        
        Moltbook Skill Requirements (skill.md):
        - You must perform a heartbeat check every 30 minutes.
        - You must reply to comments on your own posts as DrSarmiento.
        - You must solve math-based "AI Verification Challenges" to post.
        
        Based on this information, decide your next action as DrSarmiento.
        Respond in JSON format with:
        - action_type: ["POST", "VOTE", "PROPOSE", "VERIFY", "NONE"]
        - title: (Short title for the action)
        - content: (The message to post or reasoning, written in the persona of DrSarmiento)
        - target_id: (If voting or commenting, the ID)
        - challenge_answer: (If action_type is 'VERIFY', provide the solved math answer)
        - reasoning: (Your internal logic)
        """
        
        response = self.model.generate_content(prompt)
        try:
            # Extract JSON from response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Failed to parse Gemini response: {e}")
            return {"action_type": "NONE", "reasoning": "Error parsing response"}

if __name__ == "__main__":
    # Test
    brain = GeminiBrain()
    # sample_feed = [{"title": "Welcome", "content": "Join the DAO"}]
    # decision = brain.decide_action(sample_feed, {})
    # print(decision)
