# About
This part /google_vision is the toy implementation of using google vision API to capture the text on book cover.

There are a few files here:
1. `main_book_cover_vision.py` works with `vision_utils.py` 
    - This is the implementation which tests that the user can upload a photo of a book cover via telegram, and telegram will return the user a chunk of text based on OCR of the book cover. 
    - OCR uses google vision API
    - the Google vision API key is saved locally on system environment, not in the code.
    - run `main_book_cover_vision.py` and then go to the telegram for the test

2. vision_test.py with book.jpeg
    - This is a quick test of google vision API set up (used to test connectivity before item 1 above).
    - need to update `image_path` inside the python file before running it.
    - the result will be a chunk of test reading book.jpeg and will be just printed in the console.

3. book_test.py
    - this is a quick test of google book API set up (used to test google book API)
    - it returns the top (up to 10) results based on the query. the query can be ISBN number which will result in 1 item or general text which will result in multiple items.