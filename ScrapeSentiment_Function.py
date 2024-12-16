import os
import csv
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


# Load Hugging Face sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


# Function to analyze sentiment using DistilBERT
def analyze_sentiment_bert(text):
    result = sentiment_analyzer(text[:512])  # Truncate text to max token length (512)
    label = result[0]['label']
    score = result[0]['score']

    # Assign negative confidence score for negative sentiment
    if label == "NEGATIVE":
        score = -score
    return label, score


# Function to classify reviews into "Ending" or "Journey" categories
def classify_review(content):
    if any(keyword in content.lower() for keyword in ["ending", "final", "conclusion", "last chapter", "wrap up", "cliffhanger"]):
        return "Ending"
    elif any(keyword in content.lower() for keyword in ["journey", "plot", "story", "characters", "development"]):
        return "Journey"
    else:
        return "General"


# Function to scrape Goodreads reviews
def scrape_goodreads(url, book_title, save_folder='/Users/25rao/PycharmProjects/Project4_Books/CSV'):
    """
    Scrape reviews from Goodreads and perform sentiment analysis.

    Parameters:
        url (str): The Goodreads page URL.
        book_title (str): The title of the book (used for CSV filename).
        save_folder (str): Folder to save the CSV file.

    Returns:
        str: Path to the saved CSV file.
    """
    try:
        # Set up Selenium WebDriver with options
        options = Options()
        options.page_load_strategy = 'normal'
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Set timeouts
        driver.set_page_load_timeout(120)

        try:
            driver.get(url)
        except TimeoutException:
            driver.quit()
            raise TimeoutException("The page took too long to load. Try again later.")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Extract reviews
        reviews = soup.find_all('section', class_='ReviewText__content')

        if not reviews:
            raise ValueError("No reviews found on the provided page.")

        # Ensure the save folder exists
        os.makedirs(save_folder, exist_ok=True)

        # Define the CSV file path
        file_path = os.path.join(save_folder, f"{book_title}_reviews_sentiment.csv")

        # Save reviews and sentiment to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Review', 'Category', 'Sentiment', 'Confidence Score'])

            for review in reviews:
                content_div = review.find('div', class_='TruncatedContent__text')
                content = content_div.text.strip() if content_div else "No content"
                category = classify_review(content)
                sentiment_label, confidence_score = analyze_sentiment_bert(content)
                writer.writerow([content, category, sentiment_label, confidence_score])

        return file_path

    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")