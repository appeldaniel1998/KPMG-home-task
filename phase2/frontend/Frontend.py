import json
import gradio as gr
import requests


def sendMessageToServer(message, history, state):
    server_url = "http://localhost:8100/newMessage"

    try:
        # Send the current message and state to the server
        response = requests.post(server_url, json={
            "newMessage": message,
            "currentState": state,
            "history": history
        })

        # # Check if request was successful
        # if response.status_code == 200:
        print(f"Raw response: {response}")

        # Set encoding explicitly for Hebrew text
        response.encoding = 'utf-8'
        result = response.json()

        # Check if result is a string and parse it again
        if isinstance(result, str):
            result = json.loads(result)

        # Update state with response from server
        updated_state = result.get("state", state)
        server_response = result.get("message", "Server error")
        return server_response, updated_state
    except Exception as e:
        return sendMessageToServer(message, history, state)


def create_interface(initial_state):
    with gr.Blocks(title="Health Insurance Chat-Bot") as interface:
        state = gr.State(value=initial_state)  # state initialization

        gr.ChatInterface(
            fn=sendMessageToServer,
            type="messages",
            additional_inputs=[state],
            additional_outputs=[state]
        )
    return interface


if __name__ == "__main__":
    initialState = {
        "firstName": "",
        "lastName": "",
        "idNumber": "",
        "gender": "",
        "age": "",
        "hmoName": "",
        "hmoCardNumber": "",
        "insuranceMembershipTier": "",
        "informationIsVerified": False,
    }

    interface = create_interface(initialState)
    interface.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=8000,
        show_error=True
    )
