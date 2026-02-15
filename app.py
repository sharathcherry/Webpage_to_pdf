import streamlit as st
from iloveapi.iloveapi import ILoveApi
import requests
import json
import os
import re
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Web to PDF Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: rgba(255,255,255,0.7);
        font-size: 1.15rem;
    }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 1rem;
        padding: 2rem;
    }
    button[data-baseweb="tab"] {
        color: white !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.75rem;
        padding: 1rem;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 0.4rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.4);
        padding: 2rem 0 1rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# API CREDENTIALS
# =========================================
# NOTE: iLoveAPI requires both a Public Key and a Secret Key.
# Please replace YOUR_PUBLIC_KEY with the one from https://www.iloveapi.com/user/projects
ILOVEPDF_PUBLIC_KEY = 'project_public_3948d1848e5fee1dc431fd120ff53127_8ovxg5ae5984dfb60950e9b8655b37d482db2'
ILOVEPDF_SECRET_KEY = 'secret_key_c4f16e818e2bb2019ad52a854c1ead37_uU-kR5484f1dd22334314d0052324fc5b127c'

NVIDIA_API_KEY = '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'
NVIDIA_URL = 'https://integrate.api.nvidia.com/v1/chat/completions'


# =========================================
# AI TITLE GENERATOR
# =========================================
def ai_generate_title(url):
    """Use NVIDIA Kimi K2.5 to generate a short, descriptive PDF title from a URL."""
    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json",
        }
        payload = {
            "model": "moonshotai/kimi-k2.5",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a filename generator. Given a URL, respond with ONLY a short, "
                        "descriptive filename (3-7 words, no extension, use underscores instead of spaces). "
                        "The name should summarize what the webpage is about. "
                        "Example: for https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes "
                        "you would respond: Type_1_Diabetes_Overview_NIDDK\n"
                        "IMPORTANT: Respond with ONLY the filename, nothing else. No quotes, no explanation."
                    )
                },
                {
                    "role": "user",
                    "content": f"Generate a filename for this URL: {url}"
                }
            ],
            "max_tokens": 50,
            "temperature": 0.3,
            "top_p": 1.00,
            "stream": False,
        }

        response = requests.post(NVIDIA_URL, headers=headers, json=payload, timeout=15)

        if response.status_code == 200:
            data = response.json()
            title = data["choices"][0]["message"]["content"].strip()
            # Clean up: remove quotes, periods, weird chars
            title = title.strip('"\'`').strip()
            title = re.sub(r'[^\w\s-]', '', title)
            title = re.sub(r'\s+', '_', title)
            # Limit length
            if len(title) > 80:
                title = title[:80]
            return title if title else None
        else:
            return None

    except Exception:
        return None


def generate_filename(url, index=None, use_ai=True):
    """Generate a filename — AI-powered or fallback."""
    ai_title = None

    if use_ai:
        ai_title = ai_generate_title(url)

    if ai_title:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{ai_title}_{ts}.pdf", True  # True = AI generated
    else:
        # Fallback: extract from URL
        try:
            url_path = url.split("//")[1]
            domain = url_path.split("/")[0].replace("www.", "")
            path_parts = url_path.split("/")[1:]

            if path_parts and path_parts[-1]:
                page = path_parts[-1].split("?")[0].split("#")[0]
                page = page.replace(".html", "").replace(".htm", "").replace(".php", "")
                base = f"{domain}_{page}" if page else domain
            else:
                base = domain

            base = "".join(c if c.isalnum() or c in "-_." else "_" for c in base)
        except Exception:
            base = "webpage"
            if index is not None:
                base += f"_{index}"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_{ts}.pdf", False  # False = fallback


# =========================================
# PDF CONVERSION
# =========================================
def convert_url_to_pdf(url, page_size='A4', orientation='portrait', view_width=1024, max_retries=3):
    """Convert a URL to PDF bytes using iLovePDF."""
    import httpx
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            # Use a generous timeout (120s) to avoid timeouts on cloud deployments
            api = ILoveApi(
                public_key=ILOVEPDF_PUBLIC_KEY,
                secret_key=ILOVEPDF_SECRET_KEY,
                timeout=httpx.Timeout(120.0)
            )
            task = api.create_task('htmlpdf')
            
            # Upload the URL
            task.add_file_by_url(url)
            
            # Process the conversion
            # view_width controls the virtual screen width used to render the page.
            # Default API value is 1980px which makes content look tiny on A4.
            # 1024px gives a much more natural, readable scale.
            task.process(
                page_size=page_size,
                page_orientation=orientation,
                page_margin=20,
                single_page=False,
                view_width=view_width
            )
            
            # Download resulting PDF
            return task.download()
        except Exception as e:
            last_error = e
            error_msg = str(e)
            if 'timeout' in error_msg.lower() and attempt < max_retries:
                import time
                time.sleep(2 * attempt)  # Backoff: 2s, 4s
                continue
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                error_msg += f" (Details: {e.response.text})"
            raise Exception(f"iLovePDF Error: {error_msg}")
    
    raise Exception(f"iLovePDF Error: Failed after {max_retries} attempts — {last_error}")


def save_pdf(pdf_bytes, save_directory, filename):
    """Save PDF to disk. Returns path or None."""
    if not save_directory:
        return None
    try:
        os.makedirs(save_directory, exist_ok=True)
        path = os.path.join(save_directory, filename)
        with open(path, 'wb') as f:
            f.write(pdf_bytes)
        return path
    except Exception as e:
        st.warning(f"⚠️ Save failed: {e}")
        return None


def count_pdfs(directory):
    if directory and os.path.exists(directory):
        return len([f for f in os.listdir(directory) if f.lower().endswith('.pdf')])
    return 0


# =========================================
# SIDEBAR
# =========================================
def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ PDF Settings")

        page_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3", "A5"])
        orientation = st.selectbox("Orientation", ["portrait", "landscape"])
        view_width = st.slider(
            "Viewport Width (px)", min_value=600, max_value=2500, value=1024, step=50,
            help="Width of the virtual screen used to render the page. Lower = larger text in PDF. Default: 1024px"
        )

        st.markdown("---")

        # AI Toggle
        st.markdown('## 🤖 AI Naming <span class="ai-badge">Kimi K2.5</span>', unsafe_allow_html=True)
        use_ai = st.toggle("Use AI for filenames", value=True,
                           help="AI will read the URL and generate a descriptive filename")
        if use_ai:
            st.caption("✨ AI will summarize each page into a smart filename")
        else:
            st.caption("📝 Filenames will be based on URL path")

        st.markdown("---")

        # Save Location
        st.markdown("## 📁 Save Location")
        save_mode = st.radio("Save method:", ["Batch Folder", "Custom Directory"])

        save_directory = ""

        if save_mode == "Batch Folder":
            st.caption("Organize PDFs into named project folders.")
            batch_name = st.text_input("Batch Name", placeholder="e.g. Diabetes Research")
            base_dir = st.text_input("Base Directory", value=os.path.expanduser("~/Desktop"))
            if batch_name:
                save_directory = os.path.join(base_dir, batch_name)
        else:
            st.caption("Specify the exact folder path.")
            save_directory = st.text_input("Directory Path", value=os.path.expanduser("~/Desktop/PDFs"))

        if save_directory:
            st.success(f"📂 `{save_directory}`")
            n = count_pdfs(save_directory)
            if n > 0:
                st.metric("Existing PDFs", n)

        st.markdown("---")

        # Quick Examples
        st.markdown("## 📌 Quick Examples")
        examples = {
            "Example.com": "https://example.com",
            "GitHub": "https://github.com",
            "Wikipedia": "https://wikipedia.org",
            "Type 1 Diabetes": "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes",
        }
        selected = st.selectbox("Load example", ["-- select --"] + list(examples.keys()))
        example_url = examples.get(selected, "")

    return page_size, orientation, view_width, save_directory, example_url, use_ai


# =========================================
# SINGLE URL
# =========================================
def process_single(url, page_size, orientation, view_width, save_directory, use_ai):
    if not url:
        st.error("⚠️ Please enter a URL.")
        return
    if not url.startswith(("http://", "https://")):
        st.error("⚠️ URL must start with http:// or https://")
        return

    with st.spinner(f"🔄 Converting **{url}** …"):
        try:
            pdf_bytes = convert_url_to_pdf(url, page_size, orientation, view_width)

            with st.spinner("🤖 Generating smart filename …" if use_ai else ""):
                filename, was_ai = generate_filename(url, use_ai=use_ai)

            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_filename = filename
            st.session_state.conversion_ok = True

            mb = len(pdf_bytes) / 1024 / 1024
            st.success(f"✅ Done! ({mb:.2f} MB)")

            # Show filename with AI badge
            if was_ai:
                st.markdown(f'📝 Filename: **{filename}** <span class="ai-badge">AI Generated</span>', unsafe_allow_html=True)
            else:
                st.markdown(f"📝 Filename: **{filename}**")

            # Download button
            st.download_button(
                "📥 Download PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

            path = save_pdf(pdf_bytes, save_directory, filename)
            if path:
                st.info(f"💾 Saved to:\n`{path}`")
                st.metric("PDFs in folder", count_pdfs(save_directory))

        except Exception as e:
            st.error(f"❌ {e}")


# =========================================
# BULK URLS
# =========================================
def process_bulk(urls_text, page_size, orientation, view_width, save_directory, use_ai):
    urls = [u.strip() for u in urls_text.strip().splitlines() if u.strip()]

    if not urls:
        st.error("⚠️ Enter at least one URL.")
        return

    st.info(f"🔄 Processing **{len(urls)}** URLs …")
    progress = st.progress(0)
    status = st.empty()

    ok = 0
    fails = []
    filenames = []

    for i, url in enumerate(urls):
        status.text(f"Converting {i+1}/{len(urls)}: {url}")
        try:
            if not url.startswith(("http://", "https://")):
                raise Exception("URL must start with http:// or https://")

            pdf_bytes = convert_url_to_pdf(url, page_size, orientation, view_width)
            filename, was_ai = generate_filename(url, index=i, use_ai=use_ai)
            filenames.append((filename, was_ai, url, pdf_bytes))

            if save_directory:
                save_pdf(pdf_bytes, save_directory, filename)
            ok += 1
        except Exception as e:
            fails.append((url, str(e)))

        progress.progress((i + 1) / len(urls))

    status.empty()
    progress.empty()

    # Summary
    st.markdown("---")
    st.success("✅ **Conversion Complete!**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(urls))
    c2.metric("Success", ok)
    c3.metric("Failed", len(fails))

    if save_directory:
        n = count_pdfs(save_directory)
        st.info(f"📂 Saved to: `{save_directory}`\n\n📊 Total PDFs: **{n}**")

    # Show generated filenames with download buttons
    if filenames:
        with st.expander(f"� Download {len(filenames)} PDFs", expanded=True):
            for idx, (fname, was_ai, url, pdf_data) in enumerate(filenames):
                badge = ' <span class="ai-badge">AI</span>' if was_ai else ""
                st.markdown(f"• **{fname}**{badge}<br><small style='color:gray'>{url}</small>", unsafe_allow_html=True)
                st.download_button(
                    f"📥 Download",
                    data=pdf_data,
                    file_name=fname,
                    mime="application/pdf",
                    key=f"bulk_dl_{idx}",
                    use_container_width=True,
                )

    if fails:
        with st.expander(f"⚠️ {len(fails)} Failed"):
            for url, err in fails:
                st.error(f"**{url}**\n{err}")


# =========================================
# MAIN
# =========================================
def main():
    st.markdown("""
        <div class="main-header">
            <h1>📄 Web to PDF Converter</h1>
            <p>Convert any web page to a professional PDF • AI-powered filenames</p>
        </div>
    """, unsafe_allow_html=True)

    page_size, orientation, view_width, save_directory, example_url, use_ai = render_sidebar()

    _, center, _ = st.columns([1, 3, 1])

    with center:
        tab_single, tab_bulk = st.tabs(["📄 Single URL", "📚 Bulk URLs"])

        with tab_single:
            with st.form("single_form"):
                url = st.text_input("🌐 Website URL", value=example_url, placeholder="https://example.com")
                submitted = st.form_submit_button("🚀 Convert to PDF", use_container_width=True, type="primary")

            if submitted:
                process_single(url, page_size, orientation, view_width, save_directory, use_ai)

        with tab_bulk:
            with st.form("bulk_form"):
                st.caption("Enter one URL per line.")
                bulk_text = st.text_area(
                    "📋 URLs", height=200,
                    placeholder="https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3",
                )
                submitted_bulk = st.form_submit_button("🚀 Convert All to PDF", use_container_width=True, type="primary")

            if submitted_bulk:
                process_bulk(bulk_text, page_size, orientation, view_width, save_directory, use_ai)



    st.markdown('<div class="footer">Powered by iLovePDF API • AI by NVIDIA Kimi K2.5 • Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
