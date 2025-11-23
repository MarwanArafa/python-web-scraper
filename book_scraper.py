import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URL (Safe for testing/portfolio)
URL = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"

def scrape_books():
    print(f"[*] Connecting to {URL}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error: Failed to connect (Status Code: {response.status_code})")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    print(f"✅ Found {len(books)} books. Extracting data...")

    # Open CSV file to save data
    with open('science_books_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Availability", "Rating"]) # Header

        count = 0
        for book in books:
            # Extract Title
            title = book.h3.a['title']
            
            # Extract Price
            price = book.find('p', class_='price_color').text
            
            # Extract Availability
            availability = book.find('p', class_='instock availability').text.strip()
            
            # Extract Rating
            rating_class = book.find('p', class_='star-rating')['class']
            rating = rating_class[1] # e.g., "Three"

            writer.writerow([title, price, availability, rating])
            print(f" -> Scraped: {title} ({price})")
            count += 1
            
    print(f"\n🎉 Success! {count} books saved to 'science_books_data.csv'.")

if __name__ == "__main__":
    scrape_books()
