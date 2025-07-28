import json

def generate_output_json(data, output_path):
    """Write structured data to a JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save {output_path}: {e}")
