# 🚗 GetAround — Delay Analysis & Pricing Prediction
Certification CDSD — Data Science & Deployment Project

## 🔗 Production Links
- 📊 Dashboard : https://huggingface.co/spaces/Dreipfelt/getaround-dashboard
- 🔌 API : https://Dreipfelt-getaround-api.hf.space
- 📄 API Docs : https://Dreipfelt-getaround-api.hf.space/docs
- 💻 GitHub : https://github.com/Data-Science-Designer-and-Developer/Project_GetAround

## 🎯 Business Objectives
- Measure late checkout frequency and impact on subsequent rentals
- Simulate minimum delay thresholds to reduce friction
- Serve an ML pricing model via a production API

## 🤖 API — /predict
POST request example:
curl -X POST "https://Dreipfelt-getaround-api.hf.space/predict" \
     -H "Content-Type: application/json" \
     -d '{"input": [[150000, 120, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]}'

## 🛠️ Setup local
# Dashboard
streamlit run dashboard/app.py

# API
cd api
uvicorn app:app --reload

## 👤 Author
Frédéric — CDSD Candidate
Jedha Bootcamp
