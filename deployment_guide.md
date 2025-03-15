# Malicious URL Detection - Deployment Guide

## Project Structure
```
malicious-url-detection/
├── Dataset.csv
├── deploy_model.py
├── wsgi.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    └── js/
        └── main.js
```

## Prerequisites
- Python 3.8+
- Virtual Environment
- Dataset.csv file
- Required Python packages (see requirements.txt)

## Deployment Steps

1. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Variables**
Create a `.env` file:
```
FLASK_ENV=production
FLASK_APP=wsgi.py
MODEL_PATH=model/
LOG_LEVEL=INFO
PORT=8000
```

3. **Model Persistence**
- The model is trained on startup
- Consider saving the trained model using joblib for faster loading:
```python
import joblib
joblib.dump(classifier, 'model/classifier.joblib')
joblib.dump(vectorizer, 'model/vectorizer.joblib')
```

4. **Production Server**
Install and run with Gunicorn (Linux/Mac) or Waitress (Windows):
```bash
# Linux/Mac
pip install gunicorn
gunicorn wsgi:app -w 4 -b 0.0.0.0:8000

# Windows
pip install waitress
waitress-serve --port=8000 wsgi:app
```

5. **Logging Configuration**
- Logs are saved to `app.log`
- Configure log rotation to manage file size
- Set appropriate log levels for production

6. **Security Considerations**
- Use HTTPS in production
- Implement rate limiting
- Add request validation
- Consider adding authentication if needed

7. **Monitoring**
- Monitor system resources (CPU, Memory)
- Track model predictions and accuracy
- Set up error alerting
- Monitor API response times

8. **Scaling**
- Use load balancer for multiple instances
- Consider containerization (Docker)
- Implement caching if needed
- Optimize model loading and predictions

## API Endpoints

1. **Home Page**
```
GET /
Returns: HTML interface
```

2. **URL Analysis**
```
POST /analyze
Body: {"url": "https://example.com"}
Returns: {
    "status": "success",
    "prediction": "benign",
    "probabilities": {
        "benign": 0.95,
        "malware": 0.01,
        "phishing": 0.02,
        "defacement": 0.02
    }
}
```

## Maintenance

1. **Regular Tasks**
- Monitor log files
- Update dependencies
- Backup model files
- Review system performance

2. **Model Updates**
- Retrain model periodically
- Validate model accuracy
- Keep dataset updated
- Track prediction statistics

3. **Troubleshooting**
- Check log files for errors
- Monitor resource usage
- Verify model loading
- Test API endpoints

## Support
For issues or questions:
1. Check log files
2. Review error messages
3. Verify configuration
4. Contact system administrator
