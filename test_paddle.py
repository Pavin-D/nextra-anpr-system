import os
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"
from paddleocr import PaddleOCR

def main():
    try:
        # Let's try passing use_mkldnn=False if it's supported, though it might not be.
        ocr = PaddleOCR(use_textline_orientation=False, lang='en')
        
        # Pick the first image in bestplates
        img_dir = "data/bestplates"
        files = os.listdir(img_dir)
        if not files:
            print("No images found.")
            return
            
        test_file = os.path.join(img_dir, files[0])
        print(f"Testing on {test_file}")
        
        result = ocr.ocr(test_file)
        print("Result:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
