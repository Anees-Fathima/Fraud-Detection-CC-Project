from flask import Flask, render_template, request
import json

app = Flask(__name__)

def fraud_detection_logic(amount, location, device, time):
    risk_score = 0
    reasons = []

    # Rule 1: High amount
    if amount > 10000:
        risk_score += 40
        reasons.append("High transaction amount")

    # Rule 2: Unusual location
    if location not in ["India", "USA", "UK"]:
        risk_score += 30
        reasons.append("Unusual location")

    # Rule 3: Odd transaction time
    if time < "06:00" or time > "23:00":
        risk_score += 20
        reasons.append("Odd transaction time")

    # Rule 4: Suspicious device
    if device.lower() == "unknown":
        risk_score += 10
        reasons.append("Unrecognized device")

    # Determine risk level
    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "fraud_risk": risk_level,
        "risk_score": risk_score,
        "reasons": reasons
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    amount = float(request.form['amount'])
    location = request.form['location']
    device = request.form['device']
    time = request.form['time']

    result = fraud_detection_logic(amount, location, device, time)

    return render_template(
        'index.html',
        fraud_risk=result['fraud_risk'],
        risk_score=result['risk_score'],
        reasons=result['reasons']
    )


if __name__ == '__main__':
    app.run(debug=True)
