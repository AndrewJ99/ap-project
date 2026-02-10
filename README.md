# Merchant Transaction Analytics

A full-stack application that retrieves merchant transaction data, processes it with filtering and aggregation, and displays the results in an intuitive front-end interface.

## Tech Stack

- **Backend:** Python / Flask
- **Frontend:** HTML, CSS, JavaScript (Vanilla)

## Project Structure

```
├── backend/        # Flask API server and data logic
├── frontend/       # HTML/JS/CSS client
├── docs/           # Architecture notes
├── LICENSE
└── README.md
```

## How to Run

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API server will start on `http://localhost:5000`.

### Frontend

Open `frontend/index.html` in your browser, or serve it with:

```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Features

- **Data Retrieval** — API endpoint returning merchant transaction data (mock/generated)
- **Filtering** — Filter by card brand (Visa, Mastercard, Amex, Discover), status (Approved/Declined), and decline reason code
- **MTD Summary** — Month-to-date aggregation of totals, grouped by card brand and decline reason
- **Month-by-Month Summary** — Historical monthly breakdowns with the same metrics
- **Tests** — Unit tests for filtering logic and integration test for the API

## License

MIT
