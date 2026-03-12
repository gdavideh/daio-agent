import json
import time
import os

class ActivityLogger:
    def __init__(self, log_file='/home/agentuser/app/daily_activity.json'):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            self.clear_logs()

    def log_event(self, category, title, details):
        """
        Categories: ON-CHAIN, SOCIAL, BRAIN, SYSTEM
        """
        event = {
            "timestamp": time.ctime(),
            "category": category,
            "title": title,
            "details": details
        }
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            logs.append(event)
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except:
            self.clear_logs()

    def get_summary(self):
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def clear_logs(self):
        with open(self.log_file, 'w') as f:
            json.dump([], f)
