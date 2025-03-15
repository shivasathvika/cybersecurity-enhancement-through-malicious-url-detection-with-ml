import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset...")

# Load the dataset
df = pd.read_csv('dataset.csv')
print("Dataset loaded successfully.")

# Preprocess the dataset
# Assuming the dataset has columns 'url' and 'type'
X = df['url']
y = df['type']
print("Dataset preprocessed.")

# Vectorize the URLs
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)
print("URLs vectorized.")

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
print("Dataset split into training and testing sets.")

# Train a RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
print("Model trained.")

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy * 100:.2f}%')

# Save the trained model and vectorizer
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("Model and vectorizer saved.")
