import os
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from ScrapeSentiment_Function import scrape_goodreads  # Replace with actual file name containing scraping logic
from data_cleaner import process_all_books  # Replace with actual file name for data cleaning
from model_b import predict_and_update_csv  # Replace with actual file name for prediction and updates

# Initialize the main GUI window
root = tk.Tk()
root.title("Book Review Analysis")
root.geometry("800x600")

# GUI variables to display scores
ending_score_var = tk.DoubleVar()
journey_score_var = tk.DoubleVar()
predicted_score_var = tk.DoubleVar()

# Function to run the entire workflow from scraping to prediction
def run_workflow():
    # Collect user inputs from the GUI
    url = url_entry.get()
    book_title = book_title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()

    # Validate input fields
    if not url or not book_title or not author or not genre:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        # Step 1: Scrape Goodreads reviews and save them to a CSV file
        scraped_file_path = scrape_goodreads(url, book_title)
        messagebox.showinfo("Scraping Complete", f"Scraped reviews saved at {scraped_file_path}")

        # Step 2: Clean and process the scraped data
        output_folder = './CSV Model'  # Folder to store processed files
        os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists
        processed_file_path = os.path.join(output_folder, f"{book_title}_processed.csv")
        process_all_books(os.path.dirname(scraped_file_path), processed_file_path, author, genre)
        messagebox.showinfo("Processing Complete", f"Processed data saved at {processed_file_path}")

        # Step 3: Predict scores and update the processed CSV file
        updated_df = predict_and_update_csv(processed_file_path)
        messagebox.showinfo("Prediction Complete", "Predicted scores added to the processed data.")

        # Step 4: Display the results in the GUI
        display_results(updated_df, book_title)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display the results in the GUI
def display_results(df, book_title):
    # Filter the DataFrame for the specified book title
    book_data = df[df["Book Title"] == book_title]
    if book_data.empty:
        raise ValueError("No data found for the specified book.")

    # Update GUI variables with scores from the DataFrame
    ending_score_var.set(book_data["Ending Score"].values[0])
    journey_score_var.set(book_data["Journey Score"].values[0])
    predicted_score_var.set(book_data["Predicted Score"].values[0])

    # Generate needle visualizations for scores
    plot_needles(ending_score_var.get(), journey_score_var.get())

# Function to create a needle visualization for a score
def create_needle(score, title, ax):
    theta = np.linspace(0, np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)

    # Background gradient
    n_colors = 50
    for i in range(n_colors):
        ax.fill_between(
            x, 0, y,
            where=(x > -1 + 2 * i / n_colors) & (x <= -1 + 2 * (i + 1) / n_colors),
            color=plt.cm.RdBu(i / n_colors), alpha=0.8
        )

    # Outline for the semi-circle
    ax.plot(x, y, color="black", linewidth=2)

    # Needle representing the score
    needle_angle = (score / 100) * np.pi
    ax.plot([0, np.cos(needle_angle)], [0, np.sin(needle_angle)], color="black", linewidth=5)

    # Inner arc for needle base
    inner_radius = 0.2
    x_inner = inner_radius * np.cos(theta)
    y_inner = inner_radius * np.sin(theta)
    ax.fill_between(x_inner, 0, y_inner, color="black")

    # Title below the needle
    ax.text(0, -0.2, title, ha="center", va="center", fontsize=12)

    # Plot settings
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(0, 1.2)
    ax.axis("off")

# Function to plot two needle visualizations
def plot_needles(ending_score, journey_score):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Plot for Ending Score
    create_needle(ending_score, "Ending Score", axes[0])

    # Plot for Journey Score
    create_needle(journey_score, "Journey Score", axes[1])

    # Display the plots in the GUI
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Input Section: User inputs for the analysis
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

run_button = tk.Button(input_frame, text="Run Workflow", command=run_workflow, bg="blue", fg="white")
run_button.grid(row=4, columnspan=2, pady=10)

# Output Section: Display results
output_frame = ttk.LabelFrame(root, text="Results")
output_frame.pack(padx=10, pady=10, fill="x")

tk.Label(output_frame, text="Ending Score:").pack(anchor="w", padx=10, pady=5)
ending_score_label = tk.Label(output_frame, textvariable=ending_score_var)
ending_score_label.pack(anchor="w", padx=10, pady=5)

tk.Label(output_frame, text="Journey Score:").pack(anchor="w", padx=10, pady=5)
journey_score_label = tk.Label(output_frame, textvariable=journey_score_var)
journey_score_label.pack(anchor="w", padx=10, pady=5)

tk.Label(output_frame, text="Predicted Score:").pack(anchor="w", padx=10, pady=5)
predicted_score_label = tk.Label(output_frame, textvariable=predicted_score_var)
predicted_score_label.pack(anchor="w", padx=10, pady=5)

# Canvas for needle plots
canvas_frame = tk.Frame(output_frame)
canvas_frame.pack(fill="both", expand=True)

# Run the GUI application
root.mainloop()