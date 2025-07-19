from flask import Flask, request, jsonify

from phase2.backend.OpenAiClient import OpenAiClient

app = Flask(__name__)
openAiClient = OpenAiClient()


@app.route('/newMessage', methods=['POST'])
def newMessage():
    """
    Endpoint to receive messages from the frontend, analyze using OpenAI, and return the response.
    Data passed as body contains:
    - message: The message to be processed.
    - currentState: The current state of the conversation.
    :return:
    """
    requestBody = request.get_json()
    response = jsonify(openAiClient.newMessage(requestBody))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=8100)
