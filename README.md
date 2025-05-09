# TembusuExperiment
This repo serves as storing the piece-wise small experiment related to the Tembusu Library project.

Currently it carry the following experiments
1. The QR generation part, parked under `/qr_generator`, is in the form of streamlit page that can help generate a list of QR code images based on selected books.
2. The QR & Bar code scanning part, parked under `/code_reader`, demonstrates decoding QR code and bar code (for ISNB number) in a photo uploaded via telegram. 
3. The book cover reading part, parked under `/google_vision`, demonstrates extracting unstructured text from a photo of a book cover via telegram, and returning a list of search results of book information based on Google Book API via telegram in the same conversation.
