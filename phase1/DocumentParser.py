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


class DocumentParser:
    """
    Class to handle PDF document parsing and data extraction using Azure Document Intelligence and OpenAI.
    """

    def __init__(self):
        self.document_intelligence_client = DocumentIntelligenceClient(
            endpoint=documentIntelligenceEndpoint,
            credential=AzureKeyCredential(documentIntelligenceKey)
        )
        self.openAiClient = AzureOpenAI(
            azure_endpoint=openaiEndpoint,
            api_key=openAiKey,
            api_version="2024-12-01-preview"
        )

    def _analyzePDF(self, pdf_path):
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
            return None

        poller = self.document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            AnalyzeDocumentRequest(bytes_source=document_bytes),
            features=["keyValuePairs"]
        )

        result: AnalyzeResult = poller.result()
        return result

    def _analyzeExtractedData(self, extractedData) -> dict[str, str]:
        """
        Function to analyze extracted data from a PDF document and format it into a specific JSON structure.
        :param extractedData: The extracted data from document intelligence.
        :return: A dictionary containing the formatted data.
        """

        with open("./desiredFormatAndTranslation.txt", "r", encoding="utf-8") as f:
            formatAndTranslation = f.read()
        text_prompt = ("I have the following data extracted from a PDF document:\n" + str(extractedData) +
                       "\n\nI need this data in the following json format and its translation to hebrew:\n" + formatAndTranslation +
                       "\n\nNo need for any additional text, just return the json data (the keys in english, the values as specified in the form). " +
                       "If the response seems inadequate or is absent, leave the values as empty strings.")

        response = self.openAiClient.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for more deterministic output
            top_p=0.3,  # Lower top_p for more focused output
            messages=[
                ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant."),
                ChatCompletionUserMessageParam(role="user", content=text_prompt)
            ]
        )

        firstResponse = _extractJsonContent(response.choices[0].message.content)

        # First digits are not always read correctly, because there is a mark above it,
        # but always start with 0 (all Israeli phone numbers do), so if the phone number is not empty,
        # change the first digit to 0. If used in a different country, this logic may need to be changed.
        if firstResponse["landlinePhone"] != "":
            firstResponse["landlinePhone"] = '0' + firstResponse["mobilePhone"][1:]
        if firstResponse["mobilePhone"] != "":
            firstResponse["mobilePhone"] = '0' + firstResponse["mobilePhone"][1:]
        return firstResponse

    def runAnalysis(self, filePath: str) -> dict[str, str] | None:
        """
        Function to run the analysis on a PDF file and return the extracted data in a specific JSON format.
        :param filePath: str: Path to the PDF file to be analyzed.
        :return: A dictionary containing the formatted data extracted from the PDF file, or None if no data was extracted or an error occurred.
        """
        extractedResult = self._analyzePDF(filePath)
        if extractedResult is not None:
            return self._analyzeExtractedData(extractedResult)
        else:
            print("No data extracted from the PDF.")
            return None
#
#
# def main():
#     documentParser = DocumentParser()
#     documentParser.runAnalysis("../data/phase1_data/283_ex1.pdf")
#
#
# if __name__ == "__main__":
#     main()
