# Web to PDF Converter

A Streamlit web application that converts any web page to PDF using the iLovePDF API, with AI-powered filename generation via NVIDIA.

## Features

- 🎨 Modern, premium dark theme UI with gradient backgrounds
- 🌐 Convert any web page URL to PDF
- 📄 Multiple page sizes (A4, Letter, Legal, A3, A5)
- 🔄 Portrait and Landscape orientation support
- 🤖 AI-powered PDF title generation (NVIDIA Kimi K2.5)
- 📦 Bulk URL conversion with progress tracking
- 💾 Custom save directories and batch organization

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Streamlit App (Recommended)
```bash
streamlit run app.py
```

### CLI Tool
```bash
# Basic conversion
python convert_url.py https://example.com

# Custom output path and settings
python convert_url.py https://example.com -o "C:/PDFs/example.pdf" -s Letter -r landscape

# For full help
python convert_url.py --help
```

## Project Structure

```
Webpage_to_pdf/
├── app.py              # Streamlit web app (main application)
├── convert_url.py      # CLI conversion tool
├── requirements.txt    # Python dependencies
├── USAGE_GUIDE.md      # Detailed usage guide
├── LICENSE             # MIT License
└── README.md           # This file
```

## API Credentials

The app uses two APIs:
- **iLovePDF** — for HTML-to-PDF conversion (`ILOVEPDF_PUBLIC_KEY` / `ILOVEPDF_SECRET_KEY` in `app.py`)
- **NVIDIA** — for AI-powered filename generation (`NVIDIA_API_KEY` in `app.py`)

## Tech Stack

- **Frontend:** Streamlit
- **PDF Engine:** iLovePDF API (via `iloveapi` SDK)
- **AI Titles:** NVIDIA Kimi K2.5
