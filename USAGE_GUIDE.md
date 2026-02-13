# Web to PDF Converter - Quick Start Guide

## Choose Your Method

### 🌐 Method 1: Web Interface (Easy)
Use the beautiful web app with a graphical interface.

**Steps:**
1. Start the server:
   ```bash
   cd c:\Users\katuk\OneDrive\Desktop\projects\vibe\html_to_pdf
   python server.py
   ```

2. Open browser to: **http://localhost:5000**

3. Convert any URL:
   - Enter the URL
   - Choose page size and orientation
   - Enter custom filename
   - Click "Convert to PDF"
   - File downloads to your browser's default download folder

**Note:** The browser controls where files download (usually your Downloads folder). To change this, go to your browser settings.

---

### 💻 Method 2: Command Line (Full Control)
Use Python script for complete control over save location.

**Basic Usage:**
```bash
# Convert URL and save to current directory
python convert_url.py https://example.com

# Specify output filename
python convert_url.py https://example.com -o myfile.pdf

# Specify full path with custom directory
python convert_url.py https://example.com -o "C:/PDFs/example.pdf"

# Create nested directories (will be created if they don't exist)
python convert_url.py https://example.com -o "C:/MyDocuments/Work/PDFs/2024/report.pdf"
```

**Advanced Options:**
```bash
# Custom page size
python convert_url.py https://example.com -o output.pdf -s Letter

# Landscape orientation
python convert_url.py https://example.com -o output.pdf -r landscape

# Full example with all options
python convert_url.py https://example.com -o "C:/PDFs/myfile.pdf" -s A4 -r portrait
```

**Get Help:**
```bash
python convert_url.py --help
```

---

## 📂 Save Location Options

### Web Interface:
- **Where files go:** Your browser's default download folder
  - Chrome: Usually `C:\Users\YourName\Downloads`
  - Firefox: Check Settings → General → Downloads
  - Edge: Check Settings → Downloads
- **Filename:** You control this in the app
- **To change download location:** Update your browser settings

### Command Line:
- **Full control** over directory and filename
- **Auto-creates** directories if they don't exist
- **Examples:**
  - Current directory: `python convert_url.py URL -o myfile.pdf`
  - Desktop: `python convert_url.py URL -o "C:/Users/katuk/Desktop/file.pdf"`
  - Custom folder: `python convert_url.py URL -o "C:/PDFs/Work/file.pdf"`

---

## 📋 Page Size Options
- `A4` (default) - 210 × 297 mm
- `Letter` - 8.5 × 11 inches
- `Legal` - 8.5 × 14 inches
- `A3` - 297 × 420 mm
- `A5` - 148 × 210 mm

## 🔄 Orientation Options
- `portrait` (default) - Vertical
- `landscape` - Horizontal

---

## 🎯 Real-World Examples

### Example 1: Save to Desktop
```bash
python convert_url.py https://github.com -o "C:/Users/katuk/Desktop/github.pdf"
```

### Example 2: Organize by project
```bash
python convert_url.py https://documentation-url.com -o "C:/Work/ProjectX/Docs/api-docs.pdf"
```

### Example 3: Save with date
```bash
python convert_url.py https://example.com -o "C:/PDFs/2024/February/example.pdf"
```

### Example 4: Custom settings
```bash
python convert_url.py https://wikipedia.org -o "C:/PDFs/wiki.pdf" -s Letter -r landscape
```

---

## 🚀 Quick Commands

### For that diabetes URL:
```bash
# Save to Desktop
python convert_url.py "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes" -o "C:/Users/katuk/Desktop/type1-diabetes.pdf"

# Save to custom folder
python convert_url.py "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes" -o "C:/Medical/Diabetes/type1-info.pdf"
```

---

## 💡 Tips

1. **Windows paths:** Use forward slashes `/` or escape backslashes `\\`
   - Good: `"C:/PDFs/file.pdf"` or `"C:\\PDFs\\file.pdf"`
   - Also good: Use quotes for paths with spaces

2. **Auto .pdf extension:** Don't add `.pdf` - it's added automatically

3. **Create folders:** The script creates missing directories automatically

4. **Current directory:** If you don't specify `-o`, saves to current directory as `output.pdf`
