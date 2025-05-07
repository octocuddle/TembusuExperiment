import requests
import re

def looks_like_isbn(query):
    # Remove dashes and spaces
    cleaned = query.replace("-", "").replace(" ", "")
    return re.fullmatch(r"\d{10}|\d{13}", cleaned)

def search_google_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"

    # Determine if this is an ISBN search
    if looks_like_isbn(query):
        q = f"isbn:{query.replace('-', '').replace(' ', '')}"
    else:
        q = query

    params = {
        "q": q,
        "maxResults": 10,
        # "key": "YOUR_API_KEY",  # Optional
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    items = data.get("items", [])
    if not items:
        print("No books found.")
        return

    print(f"📚 Found {len(items)} book(s):\n")

    for i, item in enumerate(items, start=1):
        volume_info = item.get("volumeInfo", {})

        title = volume_info.get("title", "")
        authors = ", ".join(volume_info.get("authors", []))
        publisher = volume_info.get("publisher", "")
        published_date = volume_info.get("publishedDate", "")
        description = volume_info.get("description", "")
        page_count = volume_info.get("pageCount", "")

        # Extract ISBNs
        identifiers = volume_info.get("industryIdentifiers", [])
        isbn_10 = isbn_13 = ""
        for id_obj in identifiers:
            if id_obj["type"] == "ISBN_10":
                isbn_10 = id_obj["identifier"]
            elif id_obj["type"] == "ISBN_13":
                isbn_13 = id_obj["identifier"]

        print(f"📘 Result {i}:")
        print(f"  Title       : {title}")
        print(f"  Author(s)   : {authors}")
        print(f"  Publisher   : {publisher}")
        print(f"  Published   : {published_date}")
        print(f"  Description : {description[:200]}{'...' if len(description) > 200 else ''}")
        print(f"  ISBN-10     : {isbn_10}")
        print(f"  ISBN-13     : {isbn_13}")
        print(f"  Page Count  : {page_count}")
        print("-" * 60)

if __name__ == "__main__":

    search_google_books("147355604X")
    '''search_google_books("""NO. 1 NEW YORK TIMES BESTSELLING
AUTHOR OF SAPIENS
Yuval Noah
Harari
21 Lessons
for the
21st Century""")'''


