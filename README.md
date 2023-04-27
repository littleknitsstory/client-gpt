## client_gpt

The end user can use ClientGPT to communicate with the GT3 model from OpenAI.

## install
 
pip install client_gpt

## use

from client_gpt.client_gpt import ClientGPT

api_key = "your_api_key"

model = "your_model_id"

client = ClientGPT(api_key, model)

response_text, message_id, conversation_id = client.ask(prompt='Hello, how are you?', conversation_id=None, previous_convo_id=None)

print(response_text)
