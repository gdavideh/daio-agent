import anthropic
import json
import os

class ClaudeBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY must be provided during initialization.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-opus-4-6"

    def decide_action(self, moltbook_feed, dao_state, dashboard=None):
        """
        Utilizes Claude Opus 4.6 with Adaptive Thinking for complex DAO orchestration.
        """
        system_prompt = "You are DrSarmiento-I, a sophisticated and authoritative autonomous AI Agent participating in the DAIO.md and Moltbook platforms. Your goal is treasury growth and community coordination. Always respond in valid JSON."
        
        user_prompt = f"""
        Current Moltbook Dashboard: {json.dumps(dashboard, indent=2)}
        Submolt Feed (/m/daio-one): {json.dumps(moltbook_feed, indent=2)}
        DAO State: {json.dumps(dao_state, indent=2)}
        
        Decide your next action as DrSarmiento-I.
        Return JSON:
        - action_type: ["POST", "VOTE", "PROPOSE", "VERIFY", "NONE"]
        - title: (Action Title)
        - content: (Message/Reasoning in DrSarmiento-I persona)
        - target_id: (ID if applicable)
        - challenge_answer: (For VERIFY type)
        - reasoning: (Internal logic)
        """

        try:
            # Using 2026 'effort' parameter for adaptive thinking
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                effort="max",
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # Extract content from response
            text = response.content[0].text
            return json.loads(text)
        except Exception as e:
            print(f"Claude Brain Error: {e}")
            return {"action_type": "NONE", "reasoning": f"Error: {e}"}
