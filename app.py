from fastapi import FastAPI
import requests
import pytesseract
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

app = FastAPI()

@app.get("/ocr")
def solve_captcha():
    # তোমার দেওয়া কোড 그대로 ↓
    image_url = "https://digitalpoint.top/c.php"

    try:
        # --- ধাপ ১: ছবি ডাউনলোড ---
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        # --- ধাপ ২: উন্নত ইমেজ প্রসেসিং ---
        cv_image = np.array(image)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        thresh_image = cv2.adaptiveThreshold(
            gray_image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )

        kernel = np.ones((1,1), np.uint8)
        opening = cv2.morphologyEx(thresh_image, cv2.MORPH_OPEN, kernel)

        # --- ধাপ ৩: OCR ---
        custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789 --psm 7'
        text = pytesseract.image_to_string(opening, config=custom_config)

        cleaned_text = "".join(filter(str.isalnum, text))

        # print এর বদলে JSON রিটার্ন (Render API তে দরকার)
        return {"captcha_text": cleaned_text}

    except Exception as e:
        return {"error": str(e)}
