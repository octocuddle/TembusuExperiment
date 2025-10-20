# TembusuExperiment
This repo serves as storing the piece-wise small experiment related to the Tembusu Library project.

Currently it carry the following experiments
1. The QR generation part, parked under `/qr_generator`, is in the form of streamlit page that can help generate a list of QR code images based on selected books.
2. The QR & Bar code scanning part, parked under `/code_reader`, demonstrates decoding QR code and bar code (for ISNB number) in a photo uploaded via telegram. 
3. The book cover reading part, parked under `/google_vision`, demonstrates extracting unstructured text from a photo of a book cover via telegram, and returning a list of search results of book information based on Google Book API via telegram in the same conversation.
4. The google dialogflow multi-intent experiment part, parked under `/google_dialogflow`, was intented to test multiple intent using a dialogflow-centric bot. However, problem encountered and stuck at unable to poll image input from telegram automatically while google dialogflow is polling telegram for text message at the same time.
5. The `/Docker` carries the latest combined code to build the dockers for the complete library system.
6. The automated load test, parked under `/load_test`, is a python script to simulate multiple test user accounts (Telegram API credentials) using the chatbot in a predefined workflow - borrow-and-return - continuously without stopping in x iterations, and pause for a while to start the next cycle. The number of test accounts, iteration numbers, pause duration in seconds, number of cycles are all configurable. Test log is included for reference.