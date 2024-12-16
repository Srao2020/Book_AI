import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Load the dataset from a CSV file
df = pd.read_csv('/all_books_scores.csv')

# Initialize LabelEncoders
label_encoder_author = LabelEncoder()
label_encoder_genre = LabelEncoder()

# Fit LabelEncoders to the data
df["Author"] = label_encoder_author.fit_transform(df["Author"])
df["Genre"] = label_encoder_genre.fit_transform(df["Genre"])

# Define features and target
X = df[["Ending Score", "Journey Score", "Author", "Genre"]]
y = df["My Score"]

# Ensure target is integers between -5 and 5, excluding 0
if not all((y.isin(range(-5, 6))) & (y != 0)):
    raise ValueError("Target variable 'My Score' must be integers between -5 and 5, excluding 0.")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a classification model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, predictions))

# Predict for a new data point
new_author = "J.K. Rowling"
new_genre = "Fantasy"

# Handle new authors and genres
if new_author not in label_encoder_author.classes_:
    # Add "unknown" to the classes_
    label_encoder_author.classes_ = np.append(label_encoder_author.classes_, "unknown")
    author_encoded = label_encoder_author.transform(["unknown"])[0]
else:
    author_encoded = label_encoder_author.transform([new_author])[0]

if new_genre not in label_encoder_genre.classes_:
    # Add "unknown" to the classes_
    label_encoder_genre.classes_ = np.append(label_encoder_genre.classes_, "unknown")
    genre_encoded = label_encoder_genre.transform(["unknown"])[0]
else:
    genre_encoded = label_encoder_genre.transform([new_genre])[0]

# Create new data point
new_data = pd.DataFrame({
    "Ending Score": [-4.34],
    "Journey Score": [1.03],
    "Author": [author_encoded],
    "Genre": [genre_encoded]
})

# Predict the score
predicted_score = model.predict(new_data)
print("Predicted Score:", predicted_score[0])