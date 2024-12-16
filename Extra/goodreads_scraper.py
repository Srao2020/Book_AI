import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox

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
            messagebox.showerror("Error", "The page took too long to load. Try again later.")
            driver.quit()
            return

        # Scroll down to load more reviews (optional)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Extract reviews
        reviews = soup.find_all('section', class_='ReviewText__content')

        if not reviews:
            messagebox.showinfo("No Reviews Found", "Could not find any reviews on the provided page.")
            return

        # Define the save folder
        save_folder = '/Users/25rao/PycharmProjects/Project4_Books/CSV'
        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Define the CSV file path
        file_path = os.path.join(save_folder, f"{book_title}_reviews.csv")

        # Save reviews to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Review'])

            for review in reviews:
                # Extract the actual text from the `TruncatedContent__text` div
                content_div = review.find('div', class_='TruncatedContent__text')
                content = content_div.text.strip() if content_div else "No content"
                writer.writerow([content])

        messagebox.showinfo("Success", f"Reviews successfully saved to {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle button click
def start_scraping():
    url = url_entry.get()
    book_title = book_title_entry.get()

    if not url or not book_title:
        messagebox.showwarning("Input Error", "Please provide both the Goodreads URL and Book Title.")
        return

    scrape_goodreads(url, book_title)

# Create the UI
root = tk.Tk()
root.title("Goodreads Review Scraper")
root.geometry("400x200")

# URL input
tk.Label(root, text="Goodreads Book URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Book title input
tk.Label(root, text="Book Title:").pack(pady=5)
book_title_entry = tk.Entry(root, width=50)
book_title_entry.pack(pady=5)

# Scrape button
scrape_button = tk.Button(root, text="Scrape Reviews", command=start_scraping, bg="blue", fg="white")
scrape_button.pack(pady=20)

# Run the UI loop
root.mainloop()