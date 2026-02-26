from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import json
import numpy as np
import pandas as pd

# ── Load model and feature names ────────────────────────────────────────
pipeline = joblib.load("pipeline.pkl")

with open("feature_names.json", "r") as f:
    feature_names = json.load(f)

# ── Initialize app ──────────────────────────────────────────────────────
app = FastAPI(
    title="GetAround Pricing API",
    description="Predicts the optimal rental price per day for a car",
    version="1.0.0"
)

# ── Input schema ────────────────────────────────────────────────────────


class PredictInput(BaseModel):
    input: list

    class Config:
        json_schema_extra = {
            "example": {
                "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
            }
        }

# ── Root route ──────────────────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🚗 GetAround Pricing API</h1>
            <p>API is running!</p>
            <a href="/docs">📄 Go to Documentation</a>
        </body>
    </html>
    """

# ── /predict route ──────────────────────────────────────────────────────


@app.post("/predict")
def predict(data: PredictInput):
    # Convert input to DataFrame with correct column names
    X = pd.DataFrame(data.input, columns=feature_names)

    # Make predictions
    predictions = pipeline.predict(X)

    # Round to 2 decimals and return as list
    return {"prediction": [round(float(p), 2) for p in predictions]}

# ── /docs route ─────────────────────────────────────────────────────────


@app.get("/docs", response_class=HTMLResponse)
def documentation():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GetAround API Documentation</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; color: #333; }
            header { background: #1a1a2e; color: white; padding: 40px; text-align: center; }
            header h1 { font-size: 2.5em; margin-bottom: 10px; }
            header p { color: #aaa; font-size: 1.1em; }
            .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
            .endpoint { background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
            .endpoint h2 { font-size: 1.4em; margin-bottom: 15px; display: flex; align-items: center; gap: 12px; }
            .badge { padding: 5px 14px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }
            .post { background: #d4edda; color: #155724; }
            .get  { background: #cce5ff; color: #004085; }
            .url  { background: #1a1a2e; color: #00d4aa; padding: 12px 18px; border-radius: 8px; font-family: monospace; margin: 15px 0; }
            .section-title { font-weight: bold; margin: 20px 0 8px; color: #555; text-transform: uppercase; font-size: 0.85em; letter-spacing: 1px; }
            pre { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px; font-family: monospace; font-size: 0.9em; overflow-x: auto; }
            .param-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .param-table th { background: #f1f3f5; padding: 10px; text-align: left; font-size: 0.85em; color: #555; }
            .param-table td { padding: 10px; border-bottom: 1px solid #f1f3f5; font-size: 0.9em; }
            .tag { background: #e9ecef; padding: 2px 8px; border-radius: 4px; font-family: monospace; font-size: 0.85em; }
            footer { text-align: center; padding: 30px; color: #aaa; font-size: 0.9em; }
        </style>
    </head>
    <body>

    <header>
        <h1>🚗 GetAround Pricing API</h1>
        <p>Predict the optimal rental price per day for any car</p>
    </header>

    <div class="container">

        <div class="endpoint">
            <h2><span class="badge post">POST</span>/predict</h2>
            <p>Returns a predicted rental price per day based on the car's characteristics.</p>
            <div class="url">/predict</div>

            <div class="section-title">Input</div>
            <p>JSON body with key <span class="tag">input</span> — a list of lists (one per car).</p>

            <table class="param-table">
                <tr><th>#</th><th>Feature</th><th>Type</th><th>Example</th></tr>
                <tr><td>1</td><td>mileage</td><td>float</td><td>150000.0</td></tr>
                <tr><td>2</td><td>engine_power</td><td>float</td><td>120.0</td></tr>
                <tr><td>3</td><td>private_parking_available</td><td>bool (0/1)</td><td>1.0</td></tr>
                <tr><td>4</td><td>has_gps</td><td>bool (0/1)</td><td>1.0</td></tr>
                <tr><td>5</td><td>has_air_conditioning</td><td>bool (0/1)</td><td>1.0</td></tr>
                <tr><td>6</td><td>automatic_car</td><td>bool (0/1)</td><td>0.0</td></tr>
                <tr><td>7</td><td>has_getaround_connect</td><td>bool (0/1)</td><td>1.0</td></tr>
                <tr><td>8</td><td>has_speed_regulator</td><td>bool (0/1)</td><td>1.0</td></tr>
                <tr><td>9</td><td>winter_tires</td><td>bool (0/1)</td><td>0.0</td></tr>
            </table>

            <div class="section-title">Request Example</div>
            <pre>curl -X POST "https://your-url/predict" \
     -H "Content-Type: application/json" \
     -d '{"input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]}'</pre>

            <div class="section-title">Response Example</div>
            <pre>{"prediction": [89.5]}</pre>
        </div>

        <div class="endpoint">
            <h2><span class="badge get">GET</span>/</h2>
            <p>Health check — confirms the API is running.</p>
            <div class="url">/</div>
        </div>

        <div class="endpoint">
            <h2><span class="badge get">GET</span>/docs</h2>
            <p>This documentation page.</p>
            <div class="url">/docs</div>
        </div>

        <div class="endpoint">
            <h2>🤖 Model Information</h2>
            <table class="param-table">
                <tr><th>Property</th><th>Value</th></tr>
                <tr><td>Algorithm</td><td>XGBoost Regressor (via sklearn Pipeline)</td></tr>
                <tr><td>Target</td><td>rental_price_per_day (€)</td></tr>
                <tr><td>RMSE</td><td>~XX €</td></tr>
                <tr><td>R²</td><td>~0.XX</td></tr>
            </table>
            <p style="margin-top:12px; color:#888; font-size:0.85em;">
                ⚠️ Replace RMSE and R² with your actual results from the notebook.
            </p>
        </div>

    </div>
    <footer>GetAround Pricing API — Built with FastAPI 🚀</footer>
    </body>
    </html>
    """
