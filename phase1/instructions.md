The instructions for running the code are as follows:
* Ensure you have a recent Python installed on your machine (Python 3.12 was used for development).
* Install the required libraries by running as specified in the [requirements.txt](requirements.txt) file.
* Run the application by running the file "[DocumentParserUi.py](DocumentParserUi.py)"
* You can access the application by opening a web browser to the url: "http://127.0.0.1:8200"
* You can upload a PDF/JPG file using the provided interface (more specific instructions are included in the ui).
* The application will process the PDF file and display the extracted text in the interface.
* You may remove the uploaded file and exchange it to another file to process a different document.

Note: <br>
* Although some effort was made to reduce runtime, the application may take up to a minute to process a file.<br>
(During testing of the provided files, the runtime was ~20-40 seconds).<br> 
I believe this runtime can be significantly 
improved by optimizing the code further, but this is not within the scope of this project.<br>
* The api key and endpoint are used as local variables in the code to reduce setup time (they are not stored as environment variables).