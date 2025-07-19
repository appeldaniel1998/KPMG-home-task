import json

from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

openaiEndpoint = "https://oai-lab-test-eastus-001.openai.azure.com/"
openAiKey = "9qsKb4fIfag5vRdoqqLl1aWsH1SXJVhrtgoQdeg9XDwTXWbZMyiLJQQJ99BEACYeBjFXJ3w3AAABACOGkdkg"


def _extractJsonContent(text):
    """
    Find and extract the first complete JSON object from text.

    :param text: String containing JSON-like content.
    :return: Extracted JSON as dict if found, otherwise None.
    """
    start = text.find('{')
    if start == -1:
        return None

    brace_count = 0
    for i, char in enumerate(text[start:], start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                # Found the end of the first complete JSON object
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None

    return None


class OpenAiClient:
    def __init__(self):
        self.openAiClient = AzureOpenAI(
            azure_endpoint=openaiEndpoint,
            api_key=openAiKey,
            api_version="2024-12-01-preview"
        )

        with open("./data/alternative_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase = file.read()
        self.knowledgeBase += "\n\n"
        with open("./data/communication_clinic_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase += file.read()
        self.knowledgeBase += "\n\n"
        with open("./data/dentel_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase += file.read()
        self.knowledgeBase += "\n\n"
        with open("./data/optometry_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase += file.read()
        self.knowledgeBase += "\n\n"
        with open("./data/pragrency_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase += file.read()
        self.knowledgeBase += "\n\n"
        with open("./data/workshops_services.html", "r", encoding="utf-8") as file:
            self.knowledgeBase += file.read()
        self.knowledgeBase += "\n\n"

    def newMessage(self, newMessageAndState):
        """
        Send a new message to OpenAI and get the response.

        :param newMessageAndState: A string containing the new message and the current state of the conversation.
        :return: The response from OpenAI.
        """

        answerPrompt = f"""
        You are a chatbot assistant. Your task is to ask for information from the user (in hebrew) and receive the from him/her the following information 
        (one field at a time), verify and then answer any questions based on the knowledge base provided below.:
        1. First and last name
        2. ID number (9-digit number)
        3. Gender
        4. Age
        5. HMO name (מכבי | מאוחדת | כללית)
        6. HMO card number (9-digit number)
        7. Insurance membership tier (זהב | כסף | ארד)
        
        If the information is not valid, try to make it valid (for example space trimming, etc), but if not possible, ask for it again (without adding it to the state).
        
        If all the information is filled, present it to the use for verification and ask if it is correct. If not confirmed, ask for the incorrect information again.
        
        If all the information is already received and verified, you should return a message in hebrew that says that the 
        information is complete and the user can ask questions.
        When the user asks a question, you should answer it based on the knowledge base provided below, and answer based on the information received from the user state.
        (you are not to answer questions until all user information is received and verified).
        Return your answer in the format (must be always a valid json):\n
        {{
            "message": "<Your message in hebrew>",
            "state": <the state of the conversation after adding the received information>,
        }}
        
        Below is the last answer from the user, and the current state of the conversation and the conversation history.
        
        message from user and current state: \n{newMessageAndState}
        \n\n
        The knowledge base is as follows (in html format): \n{self.knowledgeBase}
        """


        response = self.openAiClient.chat.completions.create(
            model="gpt-4o",
            messages=[
                ChatCompletionSystemMessageParam(role="system", content="You are a helpful and friendly chatbot assistant."),
                ChatCompletionUserMessageParam(role="user", content=answerPrompt)
            ],
            max_tokens=2000
        )

        return _extractJsonContent(response.choices[0].message.content)

