from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from flask_cors import CORS
import joblib
import logging
import re
from urllib.parse import urlparse
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the trained model and vectorizer
try:
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    logging.info("Model and vectorizer loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model or vectorizer: {e}")
    model = None
    vectorizer = None

def get_domain_registration_date(domain):
    # Placeholder function to get the domain registration date
    # Implement actual logic to fetch the registration date
    return datetime.datetime(2020, 1, 1)

def get_redirection_count(url):
    # Placeholder function to get the number of redirections
    # Implement actual logic to fetch the URL and count redirections
    return 0

def check_blacklist(url):
    # Placeholder function to check if the URL is blacklisted
    # Implement actual logic to check the URL against a blacklist
    return False

def analyze_url_details(url):
    details = {
        "length": len(url),
        "has_ip": bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)),
        "has_suspicious_chars": bool(re.search(r'[\-\_\@\#\$\%\^\&\*\(\)\+\=\[\]\{\}\|\;\:\'\"\,\<\>\?\/]', url)),
        "domain_age_days": None,
        "has_https": urlparse(url).scheme == 'https',
        "num_redirections": get_redirection_count(url),
        "is_blacklisted": check_blacklist(url),
        "phishing_keywords": bool(re.search(r'login|verify|update|account|secure|bank', url, re.IGNORECASE))
    }
    
    domain = urlparse(url).netloc
    registration_date = get_domain_registration_date(domain)
    details["domain_age_days"] = (datetime.datetime.now() - registration_date).days
    
    return details

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model or vectorizer is not available'}), 500

    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    logging.info(f"Analyzing URL: {url}")

    try:
        # Vectorize the URL
        url_vectorized = vectorizer.transform([url])
        # Predict using the trained model
        prediction = model.predict(url_vectorized)
        is_malicious = prediction[0] == 1

        # Analyze URL details
        details = analyze_url_details(url)
        risk_factors = [
            details["length"] > 75,
            details["has_ip"],
            details["has_suspicious_chars"],
            details["domain_age_days"] < 30,
            not details["has_https"],
            details["num_redirections"] > 3,
            details["is_blacklisted"],
            details["phishing_keywords"]
        ]
        risk_score = sum(risk_factors) * 12.5  # Example risk score calculation

        # Generate a detailed analysis report
        analysis_report = {
            'is_malicious': is_malicious,
            'risk_score': risk_score,
            'details': details,
            'recommendations': []
        }

        if details["has_ip"]:
            analysis_report['recommendations'].append("Avoid using URLs with IP addresses. URLs with IP addresses can be risky because they are often used by attackers to hide the true destination of the link.")
        if details["has_suspicious_chars"]:
            analysis_report['recommendations'].append("Avoid URLs with suspicious characters. These characters can be used to obfuscate the URL or make it look similar to a legitimate URL.")
        if details["domain_age_days"] < 30:
            analysis_report['recommendations'].append("Be cautious with newly registered domains. Older domains are generally considered safer because they have a longer history and are less likely to be associated with recent malicious activity.")
        if not details["has_https"]:
            analysis_report['recommendations'].append("Prefer URLs with HTTPS for secure connections. HTTPS ensures data transmitted between the user and the website is secure.")
        if details["num_redirections"] > 3:
            analysis_report['recommendations'].append("Avoid URLs with multiple redirections. Multiple redirections can be a red flag as they are often used to hide the final destination of a malicious URL.")
        if details["phishing_keywords"]:
            analysis_report['recommendations'].append("Be cautious with URLs containing phishing keywords. These keywords are often used in phishing attempts to trick users into providing sensitive information.")

        logging.info(f"Prediction result for URL {url}: {'Malicious' if is_malicious else 'Safe'}")
        return jsonify(analysis_report)
    except Exception as e:
        logging.error(f"Error during prediction for URL {url}: {e}")
        return jsonify({'error': 'Error during prediction'}), 500

@app.route('/api/logout')
def logout():
    # Handle logout logic here
    return redirect(url_for('home'))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
