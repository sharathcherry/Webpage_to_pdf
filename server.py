from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pdfcrowd
import io
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your API credentials
API_USERNAME = 'sharathcherry'
API_KEY = 'b6acc869f9cab87fab16928c9fda79a9'

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/style.css')
def style():
    return send_file('style.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        data = request.json
        url = data.get('url')
        page_size = data.get('page_size', 'A4')
        orientation = data.get('orientation', 'portrait')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Create API client
        client = pdfcrowd.HtmlToPdfClient(API_USERNAME, API_KEY)
        
        # Set page size
        if page_size == 'A4':
            client.setPageSize('A4')
        elif page_size == 'Letter':
            client.setPageSize('Letter')
        elif page_size == 'Legal':
            client.setPageSize('Legal')
        elif page_size == 'A3':
            client.setPageSize('A3')
        elif page_size == 'A5':
            client.setPageSize('A5')
        
        # Set orientation
        if orientation == 'landscape':
            client.setOrientation('landscape')
        else:
            client.setOrientation('portrait')
        
        # Convert URL to PDF
        pdf_bytes = client.convertUrl(url)
        
        # Create a BytesIO object to send the PDF
        pdf_io = io.BytesIO(pdf_bytes)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='webpage.pdf'
        )
        
    except pdfcrowd.Error as e:
        return jsonify({'error': f'Pdfcrowd Error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Web to PDF Converter Server Starting...")
    print("=" * 60)
    print(f"📍 Server running at: http://localhost:5000")
    print(f"🌐 Open in browser: http://localhost:5000")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, port=5000)
