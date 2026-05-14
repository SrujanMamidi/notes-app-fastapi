# 📝 Fullstack Notes App (FastAPI + Streamlit)

A modern, decoupled, and highly responsive Note-Taking Application. Built using a robust REST API backend powered by **FastAPI** and an elegant, sticky-note styled user interface created with **Streamlit**.

---

## 🚀 Tech Stack

### **Backend**
* **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance Python framework used for building the RESTful API endpoints.
* **[Uvicorn](https://www.uvicorn.org/)**: Lightning-fast ASGI web server implementation used to run the application.
* **[Pydantic](https://docs.pydantic.dev/)**: Enforces rigid data validation, type hints, and schema definitions.
* **Storage**: Lightweight, file-based persistence using local JSON (`database/notes.json`).

### **Frontend**
* **[Streamlit](https://streamlit.io/)**: Pure Python framework turning data scripts into interactive web apps.
* **[Requests](https://requests.readthedocs.io/)**: HTTP library used to communicate with the FastAPI server.
* **Styling**: Tailored, custom CSS providing a premium layout with tilted note cards, drop shadows, and modern typography.

### **Deployments & Tools**
* **Vercel Serverless Ready**: Configured with `vercel.json` and `api/index.py` for stateless backend deployment.
* **Git/GitHub**: Version control integration.

---

## 📂 Project Architecture

```text
Notes API/
│
├── api/
│   └── index.py              # Serverless entrypoint for Vercel deployments
│
├── backend/                  # API Backend application
│   ├── database/
│   │   └── notes.json        # Persistent JSON data store
│   ├── middleware/
│   │   └── logging.py        # Custom logging middleware logic
│   ├── routes/
│   │   └── notes.py          # REST API routing endpoints
│   ├── schemas/
│   │   └── note.py           # Pydantic schemas (NoteCreate, NoteUpdate, Note)
│   ├── services/
│   │   └── note_services.py  # Core business logic layer
│   ├── utils/
│   │   └── helpers.py        # File I/O helpers for loading/saving notes
│   └── main.py               # Application entrypoint
│
├── frontend/                 # Client Frontend application
│   └── app.py                # Streamlit UI dashboard
│
├── requirements.txt          # Project dependencies
└── vercel.json               # Vercel serverless routing rules
```

---

## 🔌 API Endpoints Reference

Base URL (Local): `http://127.0.0.1:8000`

| HTTP Method | Endpoint | Request Body | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | None | Root check message |
| **GET** | `/notes/` | None | Returns a list of all saved notes |
| **GET** | `/notes/search?q=term` | None | Searches notes matching title or content |
| **GET** | `/notes/{id}` | None | Fetches a single note by UUID |
| **POST** | `/notes/` | `{"title": "...", "content": "..."}` | Creates a new note object |
| **PATCH** | `/notes/{id}` | `{"title": "...", "content": "..."}` | Partially updates an existing note |
| **DELETE**| `/notes/{id}` | None | Deletes a specified note |

---

## 💻 Running Locally

To test or run both parts of the app on your local machine:

### 1. Start the Backend API
Open a terminal, navigate to your root folder, and launch Uvicorn:
```bash
cd backend
uvicorn main:app --reload
```
*The API will be live at `http://127.0.0.1:8000` with interactive documentation available at `http://127.0.0.1:8000/docs`.*

### 2. Start the Frontend Interface
Open a second terminal window, navigate to the frontend folder, and launch Streamlit:
```bash
cd frontend
streamlit run app.py
```
*Your web interface will open automatically in your browser at `http://localhost:8501`.*

---

## 🌍 Deployment Guides

### **Option A: Production Setup (Recommended)**
Since Streamlit relies on continuous WebSocket connections and simple local JSON files don't persist on read-only serverless systems, split your services:
1. **Frontend**: Host `frontend/app.py` for free on **[Streamlit Community Cloud](https://streamlit.io/cloud)**.
2. **Backend**: Host the FastAPI server on **[Render](https://render.com/)** or **[Railway](https://railway.app/)** as a Web Service. Remember to update the `API_URL` variable in `frontend/app.py` to point to your live backend service URL.

### **Option B: Vercel Serverless Backend**
If connecting to an external database (e.g., Supabase, MongoDB Atlas), you can directly host the API on Vercel using the built-in configuration:
1. Import your GitHub repository to your **Vercel Dashboard**.
2. Keep the Framework Preset as **Other**.
3. Deploy directly. Vercel automatically maps your routes to `api/index.py` via `vercel.json`.
