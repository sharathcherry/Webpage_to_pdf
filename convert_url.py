#!/usr/bin/env python
"""
Web to PDF Converter
Convert any web page to PDF with custom save location and filename
"""

import sys
import os
import argparse
import pdfcrowd

# Your API credentials
API_USERNAME = 'sharathcherry'
API_KEY = 'b6acc869f9cab87fab16928c9fda79a9'

def convert_url_to_pdf(url, output_path=None, page_size='A4', orientation='portrait'):
    """
    Convert a URL to PDF
    
    Args:
        url: The URL to convert
        output_path: Full path where to save the PDF (directory + filename)
        page_size: Page size (A4, Letter, Legal, A3, A5)
        orientation: Page orientation (portrait or landscape)
    """
    try:
        # If no output path specified, use current directory with default name
        if not output_path:
            output_path = 'output.pdf'
        
        # Extract directory and filename
        output_dir = os.path.dirname(output_path)
        output_file = os.path.basename(output_path)
        
        # Create directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ Created directory: {output_dir}")
        
        # Ensure .pdf extension
        if not output_file.endswith('.pdf'):
            output_file += '.pdf'
            output_path = os.path.join(output_dir, output_file) if output_dir else output_file
        
        print(f"Converting URL: {url}")
        print(f"Save location: {os.path.abspath(output_path)}")
        print(f"Page size: {page_size}")
        print(f"Orientation: {orientation}")
        print("Please wait...")
        
        # Create API client
        client = pdfcrowd.HtmlToPdfClient(API_USERNAME, API_KEY)
        
        # Set page size
        client.setPageSize(page_size)
        
        # Set orientation
        client.setOrientation(orientation)
        
        # Convert URL to PDF and save to file
        client.convertUrlToFile(url, output_path)
        
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print(f"PDF saved to: {os.path.abspath(output_path)}")
        print(f"File size: {file_size_mb:.2f} MB")
        print("=" * 60)
        
    except pdfcrowd.Error as why:
        sys.stderr.write(f'\n✗ PDFCrowd Error: {why}\n')
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f'\n✗ Error: {e}\n')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert web pages to PDF with custom save location',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert with default settings (saves to current directory)
  python convert_url.py https://example.com
  
  # Specify output filename in current directory
  python convert_url.py https://example.com -o myfile.pdf
  
  # Specify full path with directory
  python convert_url.py https://example.com -o "C:/PDFs/example.pdf"
  
  # Create nested directories
  python convert_url.py https://example.com -o "C:/MyDocuments/PDFs/2024/example.pdf"
  
  # Custom page size and orientation
  python convert_url.py https://example.com -o output.pdf -s Letter -r landscape
        '''
    )
    
    parser.add_argument('url', help='URL of the web page to convert')
    parser.add_argument('-o', '--output', 
                        help='Output path (directory + filename). Default: output.pdf in current directory',
                        default='output.pdf')
    parser.add_argument('-s', '--size', 
                        choices=['A4', 'Letter', 'Legal', 'A3', 'A5'],
                        default='A4',
                        help='Page size (default: A4)')
    parser.add_argument('-r', '--orientation',
                        choices=['portrait', 'landscape'],
                        default='portrait',
                        help='Page orientation (default: portrait)')
    
    args = parser.parse_args()
    
    convert_url_to_pdf(
        url=args.url,
        output_path=args.output,
        page_size=args.size,
        orientation=args.orientation
    )

if __name__ == '__main__':
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print("=" * 60)
        print("Web to PDF Converter")
        print("=" * 60)
        print("\nUsage: python convert_url.py <URL> [options]")
        print("\nFor detailed help, run: python convert_url.py --help")
        print("=" * 60)
        sys.exit(0)
    
    main()
