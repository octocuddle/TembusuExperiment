from google.cloud import vision
import io

# Path to the image you want to test
image_path = "/Users/jing/Desktop/book.jpeg"

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    if not texts:
        print("No text detected.")
        return

    print("Detected text:")
    print(texts[0].description)

if __name__ == "__main__":
    detect_text(image_path)
