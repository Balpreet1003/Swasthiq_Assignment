# 🏥 SwasthiQ EOD Billing Dashboard

An AI-powered **End-of-Day (EOD) Billing Dashboard** built using **FastAPI**, **React (Vite)**, **SQLite**, and **Google Gemini** as part of the **SwasthiQ Technical Assignment**.

The application enables healthcare providers to upload daily billing logs, perform deterministic reconciliation, visualize revenue analytics, and generate AI-powered narrative summaries from processed billing data.

---

# 🚀 Live Demo

### Frontend

https://swasthiq-assignment-eact.vercel.app/

### Backend API

https://swasthiq-assignment-swart.vercel.app/

### Swagger Documentation

https://swasthiq-assignment-swart.vercel.app/docs

---

# ✨ Features

## 📤 Billing Upload

- Upload daily billing JSON files
- Row-level validation of billing records
- Valid records are stored in SQLite
- Invalid rows are rejected independently
- Dashboard refreshes automatically after successful upload

---

## 📋 EOD Reconciliation

- Total billed amount
- Total collected amount
- Outstanding amount
- Refund amount
- Payment mode summary

---

## 📊 Analytics Dashboard

- Revenue by hour
- Peak revenue hour
- Top medicines by quantity
- Top medicines by revenue

---

## 🤖 AI Narrative Summary

- AI-generated business summary
- Powered by Google Gemini
- Uses reconciliation and analytics data
- Deterministic numerical reporting

---

# 🛠 Tech Stack

## Frontend

- React (Vite)
- Tailwind CSS
- Axios
- Recharts
- Lucide React

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## AI

- Google Gemini API

## Deployment

- Frontend → Vercel
- Backend → Vercel

---

# 📁 Project Structure

```text
SWASTHIQ_ASSIGNMENT
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── database
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   ├── tests
│   │   ├── utils
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env.example
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   ├── layouts
│   │   ├── pages
│   │   └── App.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── sample_data
├── README.md
└── .gitignore
```

---

# 🏗️ System Architecture

```text
                    Billing JSON
                         │
                         ▼
         Upload API (/api/v1/billing/upload)
                         │
                         ▼
            Validation & Normalization
                         │
          ┌──────────────┴──────────────┐
          │                             │
     Valid Records                Rejected Rows
          │
          ▼
        SQLite Database
          │
 ┌────────┼─────────────┬──────────────┐
 │        │             │              │
 ▼        ▼             ▼              ▼
Report Analytics   AI Narrative    Upload Stats
 API      API           API
 │         │             │
 └─────────┴─────────────┘
            │
            ▼
      React Dashboard
```

---

# 📡 API Endpoints

## Upload Billing Log

**POST**

```http
/api/v1/billing/upload
```

**Content-Type**

```text
multipart/form-data
```

**Request**

```text
file=billing.json
```

**Response**

```json
{
  "uploaded_records": 18,
  "rejected_records": 2,
  "rejected_rows": []
}
```

---

## Reconciliation Report

**GET**

```http
/api/v1/report
```

**Response**

```json
{
  "total_billed_paise": 294000,
  "total_collected_paise": 280000,
  "total_refund_paise": 1000,
  "outstanding_paise": 13000,
  "payment_summary": []
}
```

---

## Analytics

**GET**

```http
/api/v1/analytics
```

Returns

- Revenue by hour
- Peak revenue hour
- Top medicines by quantity
- Top medicines by revenue

---

## AI Narrative

**GET**

```http
/api/v1/narrative
```

**Response**

```json
{
  "summary": "..."
}
```

---

# ✅ Data Consistency

The application follows a deterministic processing pipeline:

1. Every billing record is validated independently.
2. Valid records are normalized before storage.
3. Invalid records are rejected without affecting valid data.
4. All dashboard APIs read from the same SQLite database.
5. After every successful upload, the dashboard automatically refreshes.

This guarantees that every reconciliation report, analytics chart, and AI narrative is generated from the same underlying dataset.

---

# ⚙️ Backend Setup

Clone the repository.

```bash
git clone <repository-url>
cd SWASTHIQ_ASSIGNMENT/backend
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```env
DATABASE_URL=sqlite:///billing.db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
FRONTEND_URL=http://localhost:5173
```

Run the server.

```bash
uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Navigate to the frontend.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Create a `.env` file.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

> **Note:** The frontend expects `VITE_API_BASE_URL` to include the `/api/v1` prefix because all backend APIs are exposed under this route.

Run the application.

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🚀 Deployment

## Backend Environment Variables

Configure the following variables in your Vercel backend project.

```env
DATABASE_URL=sqlite:////tmp/billing.db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
FRONTEND_URL=https://swasthiq-assignment-eact.vercel.app
```

---

## Frontend Environment Variables

Configure the following variable in your Vercel frontend project.

```env
VITE_API_BASE_URL=https://swasthiq-assignment-swart.vercel.app/api/v1
```

> **Important:** The frontend API base URL must include the `/api/v1` prefix.

---

# 🌐 API Base URL

The frontend communicates with the backend using the API base URL.

### Local Development

```text
http://127.0.0.1:8000/api/v1
```

### Production

```text
https://swasthiq-assignment-swart.vercel.app/api/v1
```

The frontend appends endpoint paths automatically.

Example:

```text
GET /report
```

becomes

```text
GET https://swasthiq-assignment-swart.vercel.app/api/v1/report
```

Similarly,

```text
GET /analytics
```

becomes

```text
GET https://swasthiq-assignment-swart.vercel.app/api/v1/analytics
```

```text
GET /narrative
```

becomes

```text
GET https://swasthiq-assignment-swart.vercel.app/api/v1/narrative
```

```text
POST /billing/upload
```

becomes

```text
POST https://swasthiq-assignment-swart.vercel.app/api/v1/billing/upload
```

---

# 📂 Sample Data

A sample billing dataset is provided in the following directory.

```text
sample_data/
```

Upload the sample JSON file using the dashboard to populate the database.

---

# 📈 Future Improvements

- Historical reports
- Multi-day analytics
- CSV export
- PDF reports
- Authentication & Authorization
- Multi-clinic support
- Persistent cloud database

---

# 👨‍💻 Author

**Balpreet Singh Gill**

- **LinkedIn:** https://www.linkedin.com/in/balpreet-singh-gill-72374925b/
- **GitHub:** https://github.com/Balpreet1003

---

⭐ If you found this project helpful, consider giving the repository a star!