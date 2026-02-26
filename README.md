# 🚗 GetAround — Delay Analysis & Pricing Prediction
> Certification CDSD — Data Science & Deployment Project — Jedha Bootcamp

---

## 📌 Project Overview

GetAround is a peer-to-peer car rental platform. Late vehicle returns create friction for subsequent rentals, leading to customer dissatisfaction and cancellations.

This project addresses two strategic challenges:

- **Operational optimization** — Analyzing late checkouts and simulating minimum delay thresholds to reduce conflicts between consecutive rentals.
- **Pricing optimization** — Serving a Machine Learning model via a production API to help owners set optimal daily rental prices.

---

## 🔗 Production Links

| Service | URL |
|---------|-----|
| 📊 Dashboard | https://huggingface.co/spaces/Dreipfelt/getaround-dashboard |
| 🔌 API | https://Dreipfelt-getaround-api.hf.space |
| 📄 API Docs | https://Dreipfelt-getaround-api.hf.space/docs |
| 💻 GitHub | https://github.com/Data-Science-Designer-and-Developer/Project_GetAround |

---

## 🎯 Business Objectives

### Delay Management
- Measure how often drivers return cars late
- Quantify the impact on subsequent rentals
- Simulate different minimum delay thresholds (0 to 720 minutes)
- Help Product Management choose:
  - an optimal delay **threshold**
  - an appropriate **scope** (all cars vs Connect only)

### Pricing Optimization
- Train a ML model on car characteristics
- Serve predictions via a REST API
- Allow real-time price prediction through a `/predict` endpoint

---

## 📊 Dashboard

The interactive dashboard allows Product Managers to:
- Visualize the distribution of late checkouts
- Compare Connect vs Mobile check-in types
- Simulate the trade-off between blocked rentals and resolved issues
- Filter by scope and threshold in real time

🔗 https://huggingface.co/spaces/Dreipfelt/getaround-dashboard

---

## 🤖 Machine Learning API

### Model
| Property | Value |
|----------|-------|
| Algorithm | Random Forest Regressor |
| Target | rental_price_per_day (€) |
| R² score | ~0.68 |
| Features | 28 (mileage, engine_power, fuel, color, car_type, options...) |

### Endpoint `/predict`
- **Method** : POST
- **Input** : JSON with key `input` — list of lists
```bash
curl -X POST "https://Dreipfelt-getaround-api.hf.space/predict" \
     -H "Content-Type: application/json" \
     -d '{"input": [[150000, 120, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]}'
```

**Response** :
```json
{"prediction": [104.75]}
```

📄 Full documentation : https://Dreipfelt-getaround-api.hf.space/docs

---

## 🗂️ Repository Structure
```
Project_GetAround/
├── api/                        # FastAPI application
│   ├── app.py                  # API endpoints
│   ├── Dockerfile              # Docker configuration
│   └── feature_names.json      # Model feature names
│
├── dashboard/                  # Streamlit dashboard
│   ├── app.py                  # Dashboard application
│   └── requirements.txt
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_EDA_delays.ipynb     # Delay analysis
│   └── 02_ML_pricing.ipynb     # ML model training
│
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.10 |
| Dashboard | Streamlit, Plotly |
| API | FastAPI, Uvicorn |
| ML | Scikit-learn, Random Forest |
| Deployment | Hugging Face Spaces, Docker |
| Version Control | Git, GitHub |

---

## ⚙️ Local Setup
```bash
# Clone the repo
git clone https://github.com/Data-Science-Designer-and-Developer/Project_GetAround.git
cd Project_GetAround

# Install dependencies
pip install -r dashboard/requirements.txt

# Run the dashboard
streamlit run dashboard/app.py

# Run the API
cd api
uvicorn app:app --reload
# API available at http://localhost:8000
```

---

## 👤 Author

**Frédéric**
CDSD Candidate — Data Scientist
Jedha Bootcamp
