# Contract extractor

## Setup instructions: 

1. **Clone the repository**

```bash
git clone <YOUR_REPO_URL>
cd contract-extractor
```

2. **Create a virtual environment**

```bash
python3 -m venv .venv
```

Activate the environment:

* macOS / Linux:

```bash
source .venv/bin/activate
```

* Windows (CMD):

```cmd
.venv\Scripts\activate
```

* Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables**

Create a `.env` file in the root:

```
DATABASE_URL=sqlite:///./database.db
OPENAI_API_KEY=your_openai_api_key
```

5. **Run the server**

```bash
fastapi dev
```

Server runs at:

```
http://127.0.0.1:8000
```

7. **Access API docs** *(optional)*

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

--- 

This is my first project ever written with Python, FastAPI and LLM integration. Please keep that in mind.

Flow diagram:
<img width="1600" height="290" alt="image" src="https://github.com/user-attachments/assets/0bbf5a59-633a-40d1-a596-c034a3d3d356" />

This API has three endpoints: 

POST /api/extract
GET /api/extractions/{document_id}
GET /api/extractions

This API leverages the power of Open AI GPT-4.1 Mini model.

## What would I change?
- I would definelely use migrations for the DB side of things as it is a better way to handle database changes. 
- I would use chunks to upload PDF to LLM and would definetely use RAG instead of a public LLM API due to rate limiting and performance issues.
- I would pay attention more to validation


## How I used AI ?
AI helped me to start as I didn't know how to start or structure this project. I started with prompting it how would one go about extracting some data from a PDF file, and it pointed me in the direction of transforming the PDF text to plain text first.
After it has been converted it should be sent to our AI of choice. That put me to thinking, what can I use to get quickest results. Chat GPT suggested I should try with using a public LLM API, but it also suggested that it would be smarter to use RAG.
Through the whole proccess of writing the code for this API i used it as my "copilot" to get things done faster. For example it pointed me to the project structure, how to use dependency injection, and a lot of other things.
