# Doesn't ask for user input just uses a CSV file
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
    result = sentiment_analyzer(text[:512])[0]  # Truncate text to max token length (512)
    label = result['label']
    score = result['score']

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

# Function to scrape Goodreads reviews using Selenium
def scrape_goodreads(url, book_title):
    try:
        # Set up Selenium WebDriver with options
        options = Options()
        options.page_load_strategy = 'normal'  # Wait for full page load
        options.add_argument("--headless")  # Enable headless mode (optional)
        options.add_argument("--disable-gpu")  # Disable GPU rendering (optional)
        options.add_argument("--no-sandbox")  # Useful for some Linux setups

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Set timeouts
        driver.set_page_load_timeout(120)  # Allow more time for page load

        try:
            driver.get(url)
        except TimeoutException:
            print(f"Error: The page for '{book_title}' took too long to load. Skipping.")
            driver.quit()
            return

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Extract reviews
        reviews = soup.find_all('section', class_='ReviewText__content')

        if not reviews:
            print(f"No reviews found for '{book_title}'.")
            return

        # Define the save folder
        save_folder = './data/my_rawdata' # MEHHHHH
        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Define the CSV file path with new naming convention
        file_path = os.path.join(save_folder, f"{book_title}_reviews_sentiment.csv")

        # Save reviews and sentiment to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Review', 'Category', 'Sentiment', 'Confidence Score'])

            for review in reviews:
                # Extract the actual text from the `TruncatedContent__text` div
                content_div = review.find('div', class_='TruncatedContent__text')
                content = content_div.text.strip() if content_div else "No content"

                # Classify review
                category = classify_review(content)

                # Perform sentiment analysis
                sentiment_label, confidence_score = analyze_sentiment_bert(content)

                # Write to CSV
                writer.writerow([content, category, sentiment_label, confidence_score])

        print(f"Reviews for '{book_title}' successfully saved to {file_path}")

    except Exception as e:
        print(f"Error scraping '{book_title}': {e}")

# Function to process books from CSV file
def process_books_from_csv(csv_file):
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) < 2:
                    print("Invalid row format. Skipping.")
                    continue

                book_title, url = row[0], row[1]
                print(f"Processing: {book_title}")
                scrape_goodreads(url, book_title)
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

# Run the script
if __name__ == "__main__":
    csv_file_path = "/Users/25rao/PycharmProjects/Project4_Books/Bad_Endings_Books.csv"  # Replace with your CSV file path
    process_books_from_csv(csv_file_path)