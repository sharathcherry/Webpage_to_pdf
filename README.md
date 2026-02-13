# Web to PDF Converter

A beautiful web application that converts any web page to PDF using the Pdfcrowd API.

## Features

- 🎨 Modern, premium dark theme UI with animations
- 🌐 Convert any web page URL to PDF
- 📄 Multiple page sizes (A4, Letter, Legal, A3, A5)
- 🔄 Portrait and Landscape orientation support
- ⚡ Fast conversion with real-time feedback
- 💾 Automatic download of generated PDFs

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the server:**
   ```bash
   python server.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Convert a web page:**
   - Enter a URL (e.g., `https://example.com`)
   - Or click one of the quick example buttons
   - Choose page size and orientation
   - Click "Convert to PDF"
   - Your PDF will download automatically!

## API Credentials

The app uses the Pdfcrowd API. The demo credentials are included, but you can replace them in `server.py`:

```python
API_USERNAME = 'your_username'
API_KEY = 'your_api_key'
```

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python Flask
- **API:** Pdfcrowd

## Project Structure

```
html_to_pdf/
├── index.html          # Main HTML file
├── style.css           # Styles and design system
├── script.js           # Frontend JavaScript
├── server.py           # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Notes

- The server runs on port 5000 by default
- CORS is enabled for local development
- Press Ctrl+C to stop the server
