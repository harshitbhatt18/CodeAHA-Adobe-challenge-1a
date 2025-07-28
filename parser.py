import pdfplumber
from collections import Counter, defaultdict
import re
import unicodedata


def clean_text(text):
    """
    Normalize, de-duplicate OCR characters, and remove extra spacing.
    """
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'([A-Za-z])\1{1,}', r'\1', text)  # Collapse repeated letters
    text = re.sub(r'\s{2,}', ' ', text)  # Remove extra spaces
    return text.strip()


def extract_pdf_data(pdf_path):
    """
    Extracts title and outline from a general PDF.
    Returns JSON-compatible dictionary with 'title' and 'outline'.
    """
    title = ""
    outline = []

    with pdfplumber.open(pdf_path) as pdf:
        all_font_sizes = []
        all_chars = []
        page_dims = {}

        for page in pdf.pages:
            chars = page.chars
            all_chars.extend([(char, page.page_number, page.width, page.height) for char in chars])
            all_font_sizes.extend([round(char["size"], 1) for char in chars])
            page_dims[page.page_number] = (page.width, page.height)

        if not all_font_sizes:
            return {"title": "", "outline": []}

        body_font_size = Counter(all_font_sizes).most_common(1)[0][0]

        # Group characters into lines by Y-coordinate
        line_map = defaultdict(list)
        for char, page_num, width, height in all_chars:
            y = round(char["top"], 1)
            line_map[(page_num, y)].append((char, width, height))

        lines_by_page = defaultdict(list)

        for (page_num, y), items in line_map.items():
            chars = [x[0] for x in items]
            width, height = items[0][1], items[0][2]
            sorted_chars = sorted(chars, key=lambda c: c['x0'])
            line_text = ''.join(c['text'] for c in sorted_chars)
            font_sizes = [c['size'] for c in sorted_chars]
            avg_size = sum(font_sizes) / len(font_sizes)
            fontnames = [c['fontname'] for c in sorted_chars]

            cleaned = clean_text(line_text)
            if len(cleaned.strip()) < 4:
                continue

            is_bold = any("Bold" in f for f in fontnames)
            line_x_center = (sorted_chars[0]['x0'] + sorted_chars[-1]['x1']) / 2
            is_centered = abs(line_x_center - width / 2) < 50
            is_top = y < height * 0.25

            lines_by_page[page_num].append({
                "text": cleaned,
                "avg_size": avg_size,
                "page": page_num,
                "is_bold": is_bold,
                "is_centered": is_centered,
                "is_top": is_top
            })

        # Font size groupings
        grouped_sizes = []
        threshold = 0.5
        for size in sorted(set(all_font_sizes), reverse=True):
            if not grouped_sizes or abs(grouped_sizes[-1] - size) > threshold:
                grouped_sizes.append(size)
        size_to_level = {s: f"H{i+1}" for i, s in enumerate(grouped_sizes[:4])}

        seen = set()
        candidate_titles = []
        heading_counter = Counter()

        for page_num in sorted(lines_by_page.keys()):
            for entry in lines_by_page[page_num]:
                size = round(entry["avg_size"], 1)
                text = entry["text"]
                level = size_to_level.get(size)
                if not level:
                    continue

                key = (text, page_num)
                if key in seen:
                    continue
                seen.add(key)
                heading_counter[text] += 1

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

                if level == "H1" and page_num == 1 and entry["is_top"] and entry["is_centered"]:
                    candidate_titles.append((text, entry))

        # Remove common repeated headings like footers/headers
        total_pages = len(pdf.pages)
        outline = [h for h in outline if heading_counter[h["text"]] <= total_pages * 0.4]

        # Title detection
        if candidate_titles:
            title = candidate_titles[0][0]
        elif outline:
            title = outline[0]["text"]

        return {
            "title": title,
            "outline": outline
        }
