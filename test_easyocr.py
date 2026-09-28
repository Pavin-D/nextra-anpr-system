import cv2
import easyocr
import os

def main():
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    img_dir = "data/bestplates"
    
    if not os.path.exists(img_dir):
        return
        
    for file in os.listdir(img_dir):
        if not file.endswith(".jpg"): continue
        
        img_path = os.path.join(img_dir, file)
        img = cv2.imread(img_path)
        
        # 1. Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Otsu Thresholding (Binarization)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # 3. Adaptive Thresholding
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        res1 = reader.readtext(img, detail=0)
        res2 = reader.readtext(thresh, detail=0)
        res3 = reader.readtext(adaptive, detail=0)
        
        print(f"File: {file}")
        print(f"Original Image: {res1}")
        print(f"Otsu Threshold: {res2}")
        print(f"Adaptive Threshold: {res3}")
        print("-" * 30)

if __name__ == "__main__":
    main()
