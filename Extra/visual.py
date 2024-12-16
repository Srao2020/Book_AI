import os
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Import your scraping and processing functions
from ScrapeSentiment_Function import scrape_goodreads  # Put the actual file name
from data_cleaner import process_single_book_csv  # Put the actual file name


# Function to process reviews using the new `process_single_book_csv`
def process_reviews_with_author_genre(file_path, author, genre):
    """
    Calls the `process_single_book_csv` function to process the reviews.

    Args:
        file_path (str): Path to the CSV file containing reviews.
        author (str): Author of the book.
        genre (str): Genre of the book.

    Returns:
        tuple: Processed ending score, journey score, and DataFrame.
    """
    # Process the reviews and get the DataFrame
    processed_df = process_single_book_csv(file_path, author, genre)

    # Extract the Ending and Journey scores
    ending_score = processed_df["Ending Score"].iloc[0]
    journey_score = processed_df["Journey Score"].iloc[0]

    return ending_score, journey_score, processed_df


# Function to load and predict using the machine learning model
def predict_score(ending_score, journey_score, author, genre):
    model_data_path = "/path/to/your/all_books_scores.csv"  # Adjust as needed
    if not os.path.exists(model_data_path):
        messagebox.showerror("Model Error", "Model data file not found.")
        return 0, 0

    df = pd.read_csv(model_data_path)
    label_encoder_author = LabelEncoder()
    label_encoder_genre = LabelEncoder()
    df["Author"] = label_encoder_author.fit_transform(df["Author"])
    df["Genre"] = label_encoder_genre.fit_transform(df["Genre"])

    X = df[["Ending Score", "Journey Score", "Author", "Genre"]]
    y = df["My Score"]
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    try:
        new_author = label_encoder_author.transform([author])[0]
        new_genre = label_encoder_genre.transform([genre])[0]
    except ValueError:
        messagebox.showerror("Prediction Error", "Author or Genre not in training data.")
        return 0, 0

    new_data = pd.DataFrame({"Ending Score": [ending_score], "Journey Score": [journey_score],
                             "Author": [new_author], "Genre": [new_genre]})
    predicted_score = model.predict(new_data)
    accuracy = accuracy_score(y, model.predict(X)) * 100

    return predicted_score[0], round(accuracy, 2)


# Function to analyze reviews and update results
def analyze_reviews():
    url = url_entry.get()
    book_title = book_title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()

    if not url or not book_title or not author or not genre:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        # Scrape reviews and save to CSV
        file_path = scrape_goodreads(url, book_title)

        # Process reviews with author and genre
        ending, journey, processed_df = process_reviews_with_author_genre(file_path, author, genre)

        # Update scores
        ending_score.set(ending)
        journey_score.set(journey)

        # Predict score using ML model
        predicted, acc = predict_score(ending, journey, author, genre)
        predicted_score.set(predicted)
        accuracy.set(acc)

        # Display results
        display_results()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to plot results
def plot_needles(ending, journey, predicted):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(["Ending", "Journey", "Predicted"], [ending, journey, predicted], color=['blue', 'green', 'orange'])
    ax.set_xlim(0, 100)
    ax.set_title("Score Needles")
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()


# Function to display results
def display_results():
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    plot_needles(ending_score.get(), journey_score.get(), predicted_score.get())

    sentiment_label.config(text=f"Ending Score: {ending_score.get()}%")
    journey_label.config(text=f"Journey Score: {journey_score.get()}%")
    predicted_label.config(text=f"Predicted Score: {predicted_score.get()}")
    accuracy_label.config(text=f"Model Accuracy: {accuracy.get()}%")


# Initialize Tkinter window
root = tk.Tk()
root.title("Book Review Analysis")
root.geometry("800x600")

# Input Section
input_frame = ttk.LabelFrame(root, text="Input Details")
input_frame.pack(padx=10, pady=10, fill="x")

tk.Label(input_frame, text="Goodreads Book URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(input_frame, width=60)
url_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Book Title:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
book_title_entry = tk.Entry(input_frame, width=60)
book_title_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Author:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
author_entry = tk.Entry(input_frame, width=60)
author_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Genre:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
genre_entry = tk.Entry(input_frame, width=60)
genre_entry.grid(row=3, column=1, padx=5, pady=5)

analyze_button = tk.Button(input_frame, text="Analyze Reviews", command=analyze_reviews, bg="blue", fg="white")
analyze_button.grid(row=4, columnspan=2, pady=10)

# Output Section
output_frame = ttk.LabelFrame(root, text="Results")
output_frame.pack(padx=10, pady=10, fill="x")

ending_score = tk.DoubleVar()
journey_score = tk.DoubleVar()
predicted_score = tk.IntVar()
accuracy = tk.DoubleVar()

sentiment_label = tk.Label(output_frame, text="Ending Score:")
sentiment_label.pack(anchor="w", padx=10, pady=5)

journey_label = tk.Label(output_frame, text="Journey Score:")
journey_label.pack(anchor="w", padx=10, pady=5)

predicted_label = tk.Label(output_frame, text="Predicted Score:")
predicted_label.pack(anchor="w", padx=10, pady=5)

accuracy_label = tk.Label(output_frame, text="Model Accuracy:")
accuracy_label.pack(anchor="w", padx=10, pady=5)

# Canvas for Needles
canvas_frame = tk.Frame(output_frame)
canvas_frame.pack(fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()
