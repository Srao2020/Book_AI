import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def predict_and_update_csv(input_csv):
   # Load the training dataset
   training_csv = '/Users/25rao/PycharmProjects/Project4_Books/all_books_scores.csv'
   training_df = pd.read_csv(training_csv)

   # Encode categorical variables in the training dataset
   label_encoder_author = LabelEncoder()
   label_encoder_genre = LabelEncoder()
   training_df["Author"] = label_encoder_author.fit_transform(training_df["Author"])
   training_df["Genre"] = label_encoder_genre.fit_transform(training_df["Genre"])

   # Define features and target for training
   X_train = training_df[["Ending Score", "Journey Score", "Author", "Genre"]]
   y_train = training_df["My Score"]

   # Ensure target is integers between -5 and 5, excluding 0
   if not all((y_train.isin(range(-5, 6))) & (y_train != 0)):
       raise ValueError("Target variable 'My Score' must be integers between -5 and 5, excluding 0.")

   # Train a classification model
   model = RandomForestClassifier(random_state=42)
   model.fit(X_train, y_train)

   # Load the input dataset for prediction
   input_df = pd.read_csv(input_csv)

   # Update label encoders with unseen labels for "Author"
   for author in input_df["Author"].unique():
       if author not in label_encoder_author.classes_:
           label_encoder_author.classes_ = np.append(label_encoder_author.classes_, author)

   # Update label encoders with unseen labels for "Genre"
   for genre in input_df["Genre"].unique():
       if genre not in label_encoder_genre.classes_:
           label_encoder_genre.classes_ = np.append(label_encoder_genre.classes_, genre)

   # Transform the input data
   input_df["Author"] = label_encoder_author.transform(input_df["Author"])
   input_df["Genre"] = label_encoder_genre.transform(input_df["Genre"])

   # Define features for prediction
   X_input = input_df[["Ending Score", "Journey Score", "Author", "Genre"]]

   # Predict for the input dataset
   input_df['Predicted Score'] = model.predict(X_input)

   return input_df

