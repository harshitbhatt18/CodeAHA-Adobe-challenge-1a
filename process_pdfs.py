import os
from parser import extract_pdf_data
from json_generator import generate_output_json  # ✅ updated import

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            print(f"[INFO] Processing {filename}...")
            parsed_data = extract_pdf_data(input_path)
            generate_output_json(parsed_data, output_path)  # ✅ updated function call
            print(f"[INFO] Saved to {output_filename}")

if __name__ == "__main__":
    process_all_pdfs()
