# doesn't multiply by 10 and round
import os
import pandas as pd

# Function to process each book file and append data to a master DataFrame
def process_book_csv(file_path, master_df):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Ensure necessary columns exist
    if not all(col in df.columns for col in ['Category', 'Confidence Score']):
        print(f"Skipping {file_path}: Missing required columns.")
        return master_df

    # Calculate average scores for each category
    ending_score = df[df['Category'] == 'Ending']['Confidence Score'].mean()
    journey_score = df[df['Category'] == 'Journey']['Confidence Score'].mean()

    # Handle cases where no reviews exist for a category
    ending_score = ending_score if pd.notna(ending_score) else 0
    journey_score = journey_score if pd.notna(journey_score) else 0

    # Extract the book title from the file name by removing "_reviews_sentiment"
    original_name = os.path.basename(file_path)
    book_title = original_name.replace('_reviews_sentiment', '').replace('.csv', '')

    # Check if the book already exists in the master DataFrame
    if book_title in master_df['Book Title'].values:
        print(f"Skipping duplicate entry for book: {book_title}")
        return master_df

    # Create a new DataFrame with scores and the book title
    new_row = pd.DataFrame({
        'Book Title': [book_title],
        'Ending Score': [ending_score],
        'Journey Score': [journey_score],
        'My Score': [0]  # Initialize "My Score" column with a default value
    })

    # Use pd.concat to add the new row to the master DataFrame
    master_df = pd.concat([master_df, new_row], ignore_index=True)
    return master_df

# Folder path and output file
input_folder = '/Users/25rao/PycharmProjects/Project4_Books/my_rawdata'
output_file = '/all_books_scores.csv'

# Check if the output file already exists and load it
if os.path.exists(output_file):
    master_df = pd.read_csv(output_file)
else:
    # Create an empty DataFrame to store all processed data
    master_df = pd.DataFrame(columns=['Book Title', 'Ending Score', 'Journey Score', 'My Score'])

# Loop through all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # Only process CSV files
        file_path = os.path.join(input_folder, filename)
        master_df = process_book_csv(file_path, master_df)

# Sort the combined DataFrame by 'Book Title' in alphabetical order
master_df = master_df.sort_values(by='Book Title')

# Save the sorted DataFrame to a single CSV file
master_df.to_csv(output_file, index=False)
print(f"All data combined, sorted, and saved to: {output_file}")
