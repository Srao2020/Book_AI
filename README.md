# Book Review Analysis System

## Overview
This project automates the process of analyzing book reviews and predicting whether I would enjoy a book, specifically focusing on its ending and overall journey. The system integrates web scraping, sentiment analysis, machine learning predictions, and a graphical user interface (GUI) for user-friendly interaction. This program prevents the need to spoil an ending and ensures that I can read a book knowing I will like it.
### Key Features
1. **Scraping Book Reviews:** Scrapes reviews from Goodreads using the provided link.
2. **Sentiment Analysis:** Analyzes the sentiment of reviews and categorizes them into "Ending" or "Journey".
3. **Predictive Model:** Uses a trained Random Forest Classifier to predict the user's score based on Ending and Journey sentiment scores.
4. **Visualization:** Displays results as intuitive needle visualizations.
5. **Data Integration:** Builds and updates a dataset of books, authors, and genres the user has interacted with.

## Workflow
The project follows a structured workflow:
1. **Input:**
   - Book Title
   - Author
   - Genre
   - Goodreads Review Link
2. **Processing:**
   - Scrapes reviews using Selenium and BeautifulSoup.
   - Performs sentiment analysis using a pre-trained `DistilBERT` model.
   - Classifies sentiments into "Ending" and "Journey" categories.
3. **Prediction:**
   - Predicts a score (-5 to 5) using a machine learning model trained on prior book preferences.
4. **Output:**
   - Displays Ending Score, Journey Score, and Predicted Score.
   - Visualizes scores using needle gauges.

## File Structure
The project is modularized for ease of maintenance and extension:

```
├── main.py                      # Main GUI Application
├── ScrapeSentiment_Function.py  # Web scraping and sentiment analysis logic
├── data_cleaner.py              # Processes raw review data and prepares it for predictions
├── model_b.py                   # Predictive model using Random Forest
├── README.md                    # Project documentation
├── requirements.txt             # List of dependencies
├── CSV/                         # Folder for storing scraped reviews
└── CSV Model/                   # Folder for processed data with predictions
```

## Setup Instructions
Follow these steps to set up and run the project:

### 1. Prerequisites
Ensure the following dependencies are installed:
- Python 3.8+
- Selenium
- BeautifulSoup4
- Transformers (Hugging Face)
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

### 2. Installation
1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Install a ChromeDriver for Selenium:
   - Download ChromeDriver matching your browser version from [ChromeDriver Download](https://chromedriver.chromium.org/downloads).
   - Place the executable in your system PATH or specify its location in the code.

### 3. Using the Application
1. **Input Required Details:**
   - Goodreads Book URL
   - Book Title
   - Author
   - Genre
2. **Workflow Execution:**
   - Scrapes reviews from Goodreads.
   - Processes and categorizes reviews into "Ending" and "Journey".
   - Predicts a score using the trained model.
3. **View Results:**
   - Ending and Journey scores are displayed as needle visualizations.
   - Predicted Score is prominently displayed.

## Core Components

### 1. `main.py` - Main Application
- Provides a GUI for user input and results visualization.
- Calls scraping, processing, and prediction functions in sequence.
- Visualizes scores using Matplotlib.

### 2. `ScrapeSentiment_Function.py` - Web Scraping and Sentiment Analysis
- Scrapes book reviews from Goodreads using Selenium.
- Classifies reviews into "Ending" or "Journey" based on keywords.
- Performs sentiment analysis using the `DistilBERT` model from Hugging Face.

### 3. `data_cleaner.py` - Data Preprocessing
- Processes raw review data and computes average sentiment scores for "Ending" and "Journey".
- Updates the book dataset with new records.

### 4. `model_b.py` - Predictive Model
- Trains a Random Forest Classifier using historical book data (Ending Score, Journey Score, Author, and Genre).
- Predicts the user's score for a new book based on input data.

## Visualization
- **Ending and Journey Scores**
- **Predicted Score**

## Future Enhancements
1. Add support for multiple review sources (e.g., Reddit, Amazon).
2. Implement recommendation logic based on prior reading preferences.
3. Integrate banned book checks and author familiarity weights.
4. Build a comprehensive book database with user ratings and read history.

---

**ChatGPT used for creation of data to build a more balanced dataset**
