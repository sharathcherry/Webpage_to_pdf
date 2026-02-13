import streamlit as st
import pdfcrowd
import io
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Web to PDF Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .stApp {
        background: transparent;
    }
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .success-box {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# API credentials
API_USERNAME = 'sharathcherry'
API_KEY = 'b6acc869f9cab87fab16928c9fda79a9'

def convert_url_to_pdf(url, page_size='A4', orientation='portrait'):
    """Convert URL to PDF and return bytes"""
    try:
        # Create API client
        client = pdfcrowd.HtmlToPdfClient(API_USERNAME, API_KEY)
        
        # Set page size
        client.setPageSize(page_size)
        
        # Set orientation
        client.setOrientation(orientation)
        
        # Convert URL to PDF bytes
        pdf_bytes = client.convertUrl(url)
        
        return pdf_bytes
        
    except pdfcrowd.Error as e:
        raise Exception(f"PDF Conversion Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Main app
def main():
    # Header
    st.markdown("""
        <h1 style='text-align: center; color: white; font-size: 3rem; margin-bottom: 0.5rem;'>
            📄 Web to PDF Converter
        </h1>
        <p style='text-align: center; color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-bottom: 2rem;'>
            Convert any web page to a professional PDF document
        </p>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ PDF Settings")
        
        page_size = st.selectbox(
            "Page Size",
            options=["A4", "Letter", "Legal", "A3", "A5"],
            index=0,
            help="Select the page size for your PDF"
        )
        
        orientation = st.selectbox(
            "Orientation",
            options=["portrait", "landscape"],
            index=0,
            help="Choose page orientation"
        )
        
        st.markdown("---")
        
        st.header("📁 Save Location")
        
        # Save mode selector
        save_mode = st.radio(
            "Choose save method:",
            options=["Batch Folder", "Custom Directory"],
            help="Batch: Organize by project name. Custom: Specify exact folder path."
        )
        
        batch_name = ""
        base_save_path = ""
        save_directory = ""
        
        if save_mode == "Batch Folder":
            st.info("💡 Organize PDFs into batch folders. Perfect for projects!")
            
            batch_name = st.text_input(
                "Batch Name",
                value="",
                placeholder="e.g., Diabetes Research, Project X",
                help="Name the batch folder for your PDFs"
            )
            
            base_save_path = st.text_input(
                "Base Directory",
                value=os.path.expanduser("~/Desktop"),
                placeholder="C:/Users/YourName/Desktop",
                help="Where to create the batch folder"
            )
            
            if batch_name:
                save_directory = os.path.join(base_save_path, batch_name)
                st.success(f"📂 Save location:\n`{save_directory}`")
                
                # Show existing files count
                if os.path.exists(save_directory):
                    pdf_count = len([f for f in os.listdir(save_directory) if f.endswith('.pdf')])
                    if pdf_count > 0:
                        st.metric("PDFs in this batch", pdf_count)
        
        else:  # Custom Directory
            st.info("💡 Specify the exact folder path where PDFs will be saved.")
            
            save_directory = st.text_input(
                "Directory Path",
                value=os.path.expanduser("~/Desktop/PDFs"),
                placeholder="C:/Users/YourName/Documents/PDFs",
                help="Full path to the directory"
            )
            
            if save_directory:
                st.success(f"📂 Save location:\n`{save_directory}`")
                
                # Show existing files count
                if os.path.exists(save_directory):
                    pdf_count = len([f for f in os.listdir(save_directory) if f.endswith('.pdf')])
                    if pdf_count > 0:
                        st.metric("PDFs in this folder", pdf_count)
        
        st.markdown("---")
        
        # Quick examples
        st.header("📌 Quick Examples")
        example_urls = {
            "Example.com": "https://example.com",
            "GitHub": "https://github.com",
            "Wikipedia": "https://wikipedia.org",
            "Type 1 Diabetes Info": "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes"
        }
        
        selected_example = st.selectbox(
            "Load example URL",
            options=["-- Select an example --"] + list(example_urls.keys())
        )
    
    # Main content area
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Add tabs for single vs bulk conversion
        tab1, tab2 = st.tabs(["📄 Single URL", "📚 Bulk URLs"])
        
        with tab1:
            with st.form("single_url_form"):
                # Single URL input
                default_url = ""
                if selected_example != "-- Select an example --":
                    default_url = example_urls[selected_example]
                
                url = st.text_input(
                    "🌐 Enter Website URL",
                    value=default_url,
                    placeholder="https://example.com",
                    help="Enter the complete URL of the webpage you want to convert"
                )
                
                # Convert button
                submit_single = st.form_submit_button(
                    "🚀 Convert to PDF",
                    use_container_width=True,
                    type="primary"
                )
            
            # Handle single URL conversion
            if submit_single and url:
                process_single_url(url, page_size, orientation, save_directory)
        
        with tab2:
            with st.form("bulk_url_form"):
                st.info("💡 Enter one URL per line to convert multiple pages at once!")
                
                bulk_urls = st.text_area(
                    "📋 Enter URLs (one per line)",
                    height=200,
                    placeholder="https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3",
                    help="Paste multiple URLs, one per line"
                )
                
                # Convert button
                submit_bulk = st.form_submit_button(
                    "🚀 Convert All URLs to PDF",
                    use_container_width=True,
                    type="primary"
                )
            
            # Handle bulk URL conversion
            if submit_bulk and bulk_urls:
                # Parse URLs
                urls_list = [url.strip() for url in bulk_urls.strip().split('\n') if url.strip()]
                
                if not urls_list:
                    st.error("⚠️ Please enter at least one URL")
                else:
                    st.info(f"🔄 Processing {len(urls_list)} URLs...")
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    success_count = 0
                    failed_urls = []
                    
                    for idx, url in enumerate(urls_list):
                        status_text.text(f"Converting {idx + 1}/{len(urls_list)}: {url}")
                        
                        try:
                            # Validate URL
                            if not url.startswith(('http://', 'https://')):
                                raise Exception("URL must start with http:// or https://")
                            
                            # Convert URL
                            pdf_bytes = convert_url_to_pdf(url, page_size, orientation)
                            
                            # Auto-generate filename
                            try:
                                url_path = url.split("//")[1]
                                domain = url_path.split("/")[0].replace("www.", "")
                                path_parts = url_path.split("/")[1:]
                                
                                if path_parts and path_parts[0]:
                                    page_name = path_parts[-1].split("?")[0].split("#")[0]
                                    if page_name and len(page_name) > 0:
                                        page_name = page_name.replace(".html", "").replace(".htm", "")
                                        filename_base = f"{domain}_{page_name}"
                                    else:
                                        filename_base = domain
                                else:
                                    filename_base = domain
                                
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"{filename_base}_{timestamp}.pdf"
                            except:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"webpage_{idx}_{timestamp}.pdf"
                            
                            # Save to directory if specified
                            if save_directory:
                                os.makedirs(save_directory, exist_ok=True)
                                full_path = os.path.join(save_directory, filename)
                                
                                with open(full_path, 'wb') as f:
                                    f.write(pdf_bytes)
                                
                                success_count += 1
                            else:
                                st.warning("⚠️ No save location specified. Skipping save.")
                        
                        except Exception as e:
                            failed_urls.append((url, str(e)))
                        
                        # Update progress
                        progress_bar.progress((idx + 1) / len(urls_list))
                    
                    # Final summary
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.markdown("---")
                    st.success(f"✅ **Conversion Complete!**")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total URLs", len(urls_list))
                    with col_b:
                        st.metric("Successful", success_count, delta_color="normal")
                    with col_c:
                        st.metric("Failed", len(failed_urls), delta_color="inverse")
                    
                    if save_directory:
                        if os.path.exists(save_directory):
                            pdf_count = len([f for f in os.listdir(save_directory) if f.endswith('.pdf')])
                            st.info(f"📂 All PDFs saved to: `{save_directory}`\n\n📊 Total PDFs in folder: **{pdf_count}**")
                    
                    # Show failed URLs if any
                    if failed_urls:
                        with st.expander(f"⚠️ View {len(failed_urls)} Failed URLs"):
                            for url, error in failed_urls:
                                st.error(f"**{url}**\n{error}")
        
        # Download button outside form (only shows if conversion was successful)
        if hasattr(st.session_state, 'conversion_success') and st.session_state.conversion_success:
            st.download_button(
                label="📥 Download PDF",
                data=st.session_state.pdf_bytes,
                file_name=st.session_state.pdf_filename,
                mime="application/pdf",
                use_container_width=True,
                type="secondary"
            )

def process_single_url(url, page_size, orientation, save_directory):
    """Process a single URL conversion"""
    if not url:
        st.error("⚠️ Please enter a URL to convert")
        return
    
    if not url.startswith(('http://', 'https://')):
        st.error("⚠️ URL must start with http:// or https://")
        return
    
    # Show loading spinner
    with st.spinner(f"🔄 Converting {url} to PDF..."):
        try:
            # Convert URL to PDF
            pdf_bytes = convert_url_to_pdf(url, page_size, orientation)
            
            # Auto-generate filename from URL
            try:
                url_path = url.split("//")[1]
                domain = url_path.split("/")[0].replace("www.", "")
                path_parts = url_path.split("/")[1:]
                
                if path_parts and path_parts[0]:
                    page_name = path_parts[-1].split("?")[0].split("#")[0]
                    if page_name and len(page_name) > 0:
                        page_name = page_name.replace(".html", "").replace(".htm", "")
                        filename_base = f"{domain}_{page_name}"
                    else:
                        filename_base = domain
                else:
                    filename_base = domain
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{filename_base}_{timestamp}.pdf"
            except:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"webpage_{timestamp}.pdf"
            
            # Store in session state for download button
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_filename = filename
            st.session_state.conversion_success = True
            
            # Success message
            file_size_mb = len(pdf_bytes) / 1024 / 1024
            st.success(f"✅ PDF generated successfully! ({file_size_mb:.2f} MB)")
            
            # Save to directory if specified
            if save_directory:
                try:
                    os.makedirs(save_directory, exist_ok=True)
                    full_path = os.path.join(save_directory, filename)
                    
                    with open(full_path, 'wb') as f:
                        f.write(pdf_bytes)
                    
                    st.info(f"💾 PDF saved to:\n`{full_path}`")
                    
                    pdf_count = len([f for f in os.listdir(save_directory) if f.endswith('.pdf')])
                    st.success(f"📊 Total PDFs in folder: {pdf_count}")
                except Exception as e:
                    st.warning(f"⚠️ Could not save to directory: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.conversion_success = False
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <p style='text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem;'>
            Powered by Pdfcrowd API • Made with ❤️ using Streamlit
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
