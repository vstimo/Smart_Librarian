# Smart Librarian

Smart Librarian is a full-stack AI-powered chat application that helps users interact with a knowledge base using natural language.  
The project consists of a FastAPI backend and a React (Vite) frontend.

---

## Features

- Chat with an AI assistant using OpenAI models
- RAG (Retrieval-Augmented Generation) for smart answers
- Modern React UI
- Dockerized for easy deployment
- Deployed on Azure Container Apps

---

## Project Structure

```
LLM HW/
│
├── app/                      # FastAPI backend
│   ├── api.py
│   ├── chat_controller.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   ├── utils/
│   ├── requirements.txt
│   └── Dockerfile
│
├── smart-librarian-ui/       # React (Vite) frontend
│   ├── src/
│   ├── .env
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml        # For local development
├── deploy-smartlib.ps1       # Azure backend deploy script
├── deploy-frontend.ps1       # Azure frontend deploy script
└── README.md
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd LLM HW
```

### 2. Set environment variables

- Edit `smart-librarian-ui/.env` and set:
  ```
  VITE_API_BASE_URL=http://localhost:8000
  ```
- Edit `app/.env` and set your OpenAI API key and model info.

### 3. Build and run with Docker Compose

```bash
docker compose up --build
```

- Frontend will be available at: [http://localhost:5173](http://localhost:5173)
- Backend will be available at: [http://localhost:8000](http://localhost:8000)

---

## Live Demo

The app is deployed on Azure and available at:

**Frontend:**  
[https://smartlib-frontend.wittywater-a44e9806.germanywestcentral.azurecontainerapps.io](https://smartlib-frontend.wittywater-a44e9806.germanywestcentral.azurecontainerapps.io)

I used free credit based on my student account, which will last for 30 days. So in case is not available when you click on it run it locally:)