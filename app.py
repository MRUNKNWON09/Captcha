import requests
import pytesseract
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from fastapi import FastAPI

app = FastAPI()

# URL of the CAPTCHA image
image_url = "https://digitalpoint.top/c.php"

@app.get("/ocr")
def solve_captcha():
    try:
        # --- Step 1: Download the Image ---
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Open the image from the downloaded content
        image = Image.open(BytesIO(response.content))

        # --- Step 2: Preprocess the Image with OpenCV ---
        # Convert the Pillow image to an OpenCV image format (numpy array)
        cv_image = np.array(image)
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply binary thresholding to get a black and white image
        # This step is crucial for removing the background and line noise
        _, threshold_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

        # --- Step 3: Extract Text from the Cleaned Image ---
        # Use Pytesseract on the clean, preprocessed image
        custom_config = r'--oem 3 --psm 6' # Configuration for Tesseract
        text = pytesseract.image_to_string(threshold_image, config=custom_config)
        
        # Clean up the output string
        cleaned_text = "".join(filter(str.isalnum, text))
        
        return {"Extracted_Text": cleaned_text}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error downloading image: {e}"}
    except pytesseract.TesseractNotFoundError:
        return {"error": "Tesseract Error: Tesseract is not installed or not in your PATH."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
