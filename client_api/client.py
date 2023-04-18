import requests
import json
import re
import uuid
import os

class ClientGPT:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.conversation_id = None
        self.session = requests.Session()


    def ask(self, prompt, conversation_id, previous_convo_id ):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'OpenAI-Integration-Name': 'python',
            'OpenAI-Integration-Version': '0.1',
        }

        data = {
            'model': self.model,
            'prompt': prompt,
        }

        if previous_convo_id is None:
            previous_convo_id = str(uuid.uuid4())

        if conversation_id is not None and len(conversation_id) == 0:
            conversation_id = None

        try:
            response = self.session.post(
                "https://chat.openai.com/backend-api/conversation",
                headers=headers,
                data=json.dumps(data)
            )
            if response.status_code == 200:
                response_text = response.text.replace("data: [DONE]", "")
                data = re.findall(r'data: (.*)', response_text)[-1]
                as_json = json.loads(data)
                return as_json["message"]["content"]["parts"][0], as_json["message"]["id"], as_json["conversation_id"]
            elif response.status_code == 401:
                if os.path.exists("auth.json"):
                    os.remove("auth.json")
                return f"[Status Code] 401 | [Response Text] {response.text}", None, None
            elif response.status_code >= 500:
                print(">> Looks like the server is either overloaded or down. Try again later.")
                return f"[Status Code] {response.status_code} | [Response Text] {response.text}", None, None
            else:
                return f"[Status Code] {response.status_code} | [Response Text] {response.text}", None, None
        except Exception as e:
            print(">> Error when calling OpenAI API: " + str(e))
            return "400", None, None