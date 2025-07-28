# PDF Outline Extractor

**Team CodeAHA** - Adobe India Hackathon 2025, Challenge 1a

A high-performance, robust PDF outline extraction solution that extracts structured document titles and hierarchical table of contents from PDF files. The system processes H1, H2, and H3 headings and outputs standardized JSON files optimized for downstream applications such as semantic search and intelligent document summarization.

---

## Overview

This solution processes PDF documents from the `/input` directory and extracts:

- **Document Title**: Primary document identifier
- **Hierarchical Outline Structure**:
  - `text`: Heading content
  - `level`: Hierarchical level (H1, H2, H3)
  - `page`: Source page number (1-indexed)

The system generates corresponding JSON files in the `/output` directory, strictly adhering to the specified schema requirements.

---

## Technical Approach

### Core Technology Stack
- **PDF Processing**: `pdfplumber` for character-level extraction with layout, font, size, and positional metadata
- **Heading Detection Algorithm**:
  - Font size bucket analysis with relative sizing logic
  - Font weight detection through name pattern matching (Bold, Heavy, etc.)
  - Position-based heuristics targeting top 25% page positioning

### Title Detection Logic
The system identifies document titles using the following criteria:
- Location: First page of document
- Position: Upper 25% of page height
- Alignment: Center-aligned text formatting
- Priority: First qualifying H1-level candidate

### Data Processing Features
- OCR noise filtering for headers, footers, timestamps, and page numbering
- Unicode normalization for multilingual document support
- Strict JSON schema compliance
- Batch processing capabilities

---

## Project Structure

```
├── Dockerfile
├── README.md
├── requirements.txt
├── process_pdfs.py          # Main processing script
├── parser.py                # PDF parsing logic
├── json_generator.py        # JSON output generation
├── input/                   # Source PDF files
│   └── *.pdf
├── output/                  # Generated JSON files
│   └── *.json
└── output_schema.json       # Output format specification
```

---

## Output Schema

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Chapter 1", "page": 1 },
    { "level": "H2", "text": "Section 1.1", "page": 2 },
    { "level": "H3", "text": "Subsection 1.1.1", "page": 2 }
  ]
}
```

---

## Installation and Deployment

### Docker Deployment (Recommended)

**Build the container:**
```bash
docker build -t adobe-challenge-1a .
```

**Execute processing:**
```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  adobe-challenge-1a
```

### Local Development Setup

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Dependencies:**
```
pdfplumber
```

---

## Key Features

- **Advanced Heading Detection**: Multi-factor analysis using font size, weight, and positioning
- **Multilingual Support**: Unicode normalization supporting CJK, Devanagari, and other character sets
- **Noise Filtering**: Intelligent removal of OCR artifacts and document metadata
- **Flexible Deployment**: Support for both CLI and containerized environments
- **Schema Compliance**: Strict adherence to specified output format
- **Batch Processing**: Efficient handling of multiple document processing
- **CPU Optimization**: Performance-tuned for CPU-only processing environments

---

## System Limitations

- **Image-based PDFs**: Does not support purely scanned documents without embedded text
- **Complex Layouts**: Multi-column layouts are processed in linear reading order
- **Font Coverage**: Advanced typography may require additional configuration

---

## Future Extensibility

The modular architecture supports:
- Nested content structure expansion
- Language-agnostic processing capabilities
- Persona-based content filtering (Challenge 1B readiness)

---

## Team

**CodeAHA Development Team**

- **Harshit Bhatt**
- **Arpit Kumar Singh**  
- **Armaan Rawat**