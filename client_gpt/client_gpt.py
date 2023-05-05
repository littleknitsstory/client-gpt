import requests
import json
import re
import uuid
import os
from typing import Tuple, Optional


class ClientGPT:
    """
    A class for interacting with the OpenAI API.
    Attributes:
        api_key (str): Your OpenAI API key.
        model (str): The ID of the GPT-3 model to use.
        conversation_id (str or None): the unique identifier of the current conversation in the OpenAI. If the value is None, a new conversation ID will be created. If a string is passed, then an existing conversation ID is used.
        session (requests.Session): A session object for making HTTP requests.
    Method:
        ask(prompt, conversation_id=None, previous_convo_id=None): Sends a prompt to the OpenAI API and returns the response.
    """

    chat_api_url = "https://api.openai.com/v1/completions"

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.conversation_id = None
        self.session = requests.Session()

    def ask(
        self, prompt: str, conversation_id: str or None, previous_convo_id: str or None
    ) -> Optional[str]:
        """
        Args:
            prompt (str): a string containing text to send to the OpenAI server.
            conversation_id (str or None): The ID of the conversation. If None, a new conversation will be started.
            previous_convo_id (str or None): The ID of the previous conversation. If None, a new conversation will be started.

        Return:
            Tuple[str, str or None, str or None]: A tuple containing the response text, the message ID, and the conversation ID.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "OpenAI-Integration-Name": "python",
            "OpenAI-Integration-Version": "0.1",
        }

        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.3,
            "n": 1,
            "echo": True,
            "stream": False,
        }

        if previous_convo_id is None:
            previous_convo_id = str(uuid.uuid4())

        if conversation_id is not None and len(conversation_id) == 0:
            conversation_id = None

        try:
            response = self.session.post(
                self.chat_api_url,
                headers=headers,
                data=json.dumps(data),
            )
            if response.status_code == 200:
                response_data = json.loads(response.text)
                choices = response_data["choices"]
                print(choices)
                if len(choices) > 0:
                    text = choices[0]["text"]
                    return text
                else:
                    return None
            elif response.status_code == 401:
                if os.path.exists("auth.json"):
                    os.remove("auth.json")
                return (
                    f"[Status Code] 401 | [Response Text] {response.text}",
                    None,
                    None,
                )
            elif response.status_code >= 500:
                print(
                    ">> Looks like the server is either overloaded or down. Try again later."
                )
                return (
                    f"[Status Code] {response.status_code} | [Response Text] {response.text}",
                    None,
                    None,
                )
            else:
                return (
                    f"[Status Code] {response.status_code} | [Response Text] {response.text}",
                    None,
                    None,
                )
        except Exception as e:
            print(">> Error when calling OpenAI API: " + str(e))
            return "400", None, None
