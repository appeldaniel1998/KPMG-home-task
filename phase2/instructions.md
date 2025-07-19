The instructions for running the code are as follows:
* Ensure you have a recent Python installed on your machine (Python 3.12 was used for development).
* Install the required libraries by running as specified in the [requirements.txt](requirements.txt) file.
* Run the backend of the application by running the file [Backend.py](backend/Backend.py)
* Run the frontend of the application by running the file [Frontend.py](frontend/Frontend.py)
* You can access the frontend by opening a web browser to the url: "http://127.0.0.1:8200"

Note: <br>
* Although some effort was made to reduce runtime, the application may take several seconds to return an answer.<br>
(During testing, the runtime was ~4-7 seconds per message).<br> 
I believe this runtime can be slightly improved by optimizing the code further.<br>
* There are some places where the code was duplicated between the 2 phases of the project. This was done to separate the phases into separate projects.<br>
(If they were part of one project, a utils file would be advised and implemented).
* The api key and endpoint are used as local variables in the code to reduce setup time (they are not stored as environment variables).