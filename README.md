# Contract extractor

## Setup Instructions

This project is fully dockerized. You do not need to install Python or manage virtual environments.

## 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd contract-extractor
```

---

## 2. Create the `.env` file

In the project root, create a `.env` file:

```
DATABASE_URL=sqlite:///./db/database.db
OPENAI_API_KEY=your_openai_api_key
```

The SQLite database file is stored in the `db/` directory and is persisted outside the container.

---

## 3. Build and run the application

```bash
docker compose up --build
```

Once running, the API is available at:

```
http://localhost:8000
```

Swagger UI documentation:

```
http://localhost:8000/docs
```

---

## 4. Stop the application

```bash
docker compose down
```

---

## 5. Database persistence (SQLite)

The `docker-compose.yml` mounts the local `db/` folder into the container:

```yaml
volumes:
  - ./db:/app/db
```

This ensures that database changes are preserved even when the container stops or is rebuilt.

---

## 6. Rebuild after code changes

Rebuild and restart:

```bash
docker compose up --build
```

Start without rebuilding:

```bash
docker compose up
```

--- 

This is my first project built with Python, FastAPI, and LLM integration, I write primarily Javascript and C#. Please keep that in mind.

## Architecture Overview

Flow diagram: <img width="1600" height="290" alt="image" src="https://github.com/user-attachments/assets/0bbf5a59-633a-40d1-a596-c034a3d3d356" />

This API exposes three endpoints:

* `POST /api/extract`
* `GET /api/extractions/{document_id}`
* `GET /api/extractions`

The service uses the OpenAI GPT-4.1 Mini model to perform contract clause extraction.

---

## What Would I Improve?

If I were to iterate on this project further, I would introduce several improvements:

* Implement proper database migrations to manage schema changes more reliably.
* Split large PDFs into chunks before sending them to the LLM, and ideally implement a RAG pipeline to avoid rate limits and improve performance and accuracy.
* Improve request validation and error handling.

---

## How I Used AI During Development

AI played a significant role in helping me structure and build this project from the ground up. Since I was unfamiliar with the overall approach, I began by asking how to extract meaningful data from a PDF file. The guidance I received helped me understand that the first step should be converting the PDF content into plain text before sending it to an LLM.

From there, I explored different ways to process the extracted text. AI suggested using a public LLM API initially but also highlighted the advantages of implementing Retrieval-Augmented Generation (RAG) as a longer-term approach.

Throughout the development process, AI acted as a “copilot,” helping me:

* design the project structure
* understand how to use dependency injection in FastAPI
* write cleaner, more maintainable Python code
* solve various implementation details more efficiently

This allowed me to focus on learning and building rather than getting stuck on technical roadblocks.

