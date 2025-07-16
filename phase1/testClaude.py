import json

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

documentIntelligenceEndpoint = "https://eastus.api.cognitive.microsoft.com/"
documentIntelligenceKey = "efbe39573b3b4e68832a5d4f6d6a391a"
openaiEndpoint = "https://oai-lab-test-eastus-001.openai.azure.com/"
openAiKey = "9qsKb4fIfag5vRdoqqLl1aWsH1SXJVhrtgoQdeg9XDwTXWbZMyiLJQQJ99BEACYeBjFXJ3w3AAABACOGkdkg"


def extract_json_content(text):
    """
    Find first { and last }

    :param text: String containing JSON-like content.
    :return: Extracted JSON as dict if found, otherwise None.
    """
    start = text.find('{')
    end = text.rfind('}')

    if start != -1 and end != -1 and start < end:
        return json.loads(text[start:end + 1])  # +1 to include the closing }
    return None


def analyzePDF(pdf_path):
    """
    Function to analyze layout and extract data from a PDF document.

    Args:
        pdf_path (str): Path to the PDF file to be analyzed.
    """
    try:
        with open(pdf_path, "rb") as f:
            document_bytes = f.read()
    except FileNotFoundError:
        print(f"File not found: {pdf_path}")
        return

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=documentIntelligenceEndpoint,
        credential=AzureKeyCredential(documentIntelligenceKey)
    )
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=document_bytes),
        features=["keyValuePairs"]
    )

    result: AnalyzeResult = poller.result()

    client = AzureOpenAI(
        azure_endpoint=openaiEndpoint,
        api_key=openAiKey,
        api_version="2024-12-01-preview"
    )

    with open("./desiredFormatAndTranslation.txt", "r", encoding="utf-8") as f:
        formatAndTranslation = f.read()
    text_prompt = ("I have the following data extracted from a PDF document:\n" + str(result) +
                   "\n\nI need this data in the following json format and its translation to hebrew:\n" + formatAndTranslation +
                   "\n\nNo need for any additional text, just return the json data (the keys in english, the values as specified in the form). " +
                   "If the response seems inadequate or is absent, leave the values as empty strings.")

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        temperature=0.3,  # Lower temperature for more deterministic output
        top_p=0.3,  # Lower top_p for more focused output
        messages=[
            ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant."),
            ChatCompletionUserMessageParam(role="user", content=text_prompt)
        ]
    )

    firstResponse = extract_json_content(response.choices[0].message.content)

    # First digits are not always read correctly, because there is a mark above it,
    # but always start with 0 (all Israeli phone numbers do), so if the phone number is not empty,
    # change the first digit to 0.
    if firstResponse["landlinePhone"] != "":
        firstResponse["landlinePhone"] = '0' + firstResponse["mobilePhone"][1:]
    if firstResponse["mobilePhone"] != "":
        firstResponse["mobilePhone"] = '0' + firstResponse["mobilePhone"][1:]
    print(firstResponse)


if __name__ == "__main__":
    analyzePDF("../data/phase1_data/283_ex1.pdf")
