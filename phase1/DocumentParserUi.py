import json

import gradio as gr

from phase1.DocumentParser import DocumentParser


def process_and_update(file):
    """
    Process the uploaded file and return the analysis results.
    :param file:
    :return:
    """
    document_parser = DocumentParser()

    if file is None:
        return "Please upload a file first", gr.File(visible=False)

    analysisAsObject = document_parser.runAnalysis(file)
    return json.dumps(analysisAsObject, indent=4, ensure_ascii=False)


def create_interface():
    with gr.Blocks(title="File Analysis Tool") as interface:
        gr.Markdown(
            """
            # 📄 File Analysis Tool
            Upload a PDF or JPG file to get analysis results in JSON format
            
            1. **Upload**: Drag and drop a PDF or JPG file into the upload area, or click to browse
            2. **Analyze**: Click the 'Analyze File' button to process your file
            3. **Results**: View the JSON output

            **Supported formats:** PDF, JPG, JPEG
            
            **Note:** Processing may take a few seconds
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                # File upload component with drag and drop
                file_input = gr.File(
                    label="📁 Upload File",
                    file_types=[".pdf", ".jpg", ".jpeg"],
                    file_count="single",
                    height=200
                )

                # Process button
                process_btn = gr.Button(
                    "Analyze File",
                    variant="primary",
                )

        with gr.Row():
            with gr.Column():
                # JSON output display
                json_output = gr.Textbox(
                    label="📋 Analysis Results (JSON)",
                    lines=15,
                    max_lines=100,
                    show_copy_button=True,
                    container=True,
                    interactive=False
                )

        process_btn.click(
            fn=process_and_update,
            inputs=[file_input],
            outputs=[json_output]
        )

    return interface


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=8200,
        show_error=True
    )
