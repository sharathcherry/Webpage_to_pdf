// =====================================
// CONFIGURATION
// =====================================
const CONFIG = {
    username: 'demo',
    apiKey: 'b6acc869f9cab87fab16928c9fda79a9',
    apiEndpoint: 'https://api.pdfcrowd.com/api/html_to_pdf/v1/convert/'
};

// =====================================
// DOM ELEMENTS
// =====================================
const elements = {
    urlInput: document.getElementById('urlInput'),
    convertBtn: document.getElementById('convertBtn'),
    clearBtn: document.getElementById('clearBtn'),
    statusMessage: document.getElementById('statusMessage'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    pageSize: document.getElementById('pageSize'),
    orientation: document.getElementById('orientation'),
    fileName: document.getElementById('fileName'),
    exampleBtns: document.querySelectorAll('.example-btn')
};

// =====================================
// UTILITY FUNCTIONS
// =====================================
function showStatus(message, type = 'info') {
    elements.statusMessage.textContent = message;
    elements.statusMessage.className = `status-message ${type}`;

    // Auto-hide after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            elements.statusMessage.style.display = 'none';
        }, 5000);
    }
}

function showLoading(show) {
    if (show) {
        elements.loadingOverlay.classList.add('active');
        elements.convertBtn.disabled = true;
    } else {
        elements.loadingOverlay.classList.remove('active');
        elements.convertBtn.disabled = false;
    }
}

function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// =====================================
// PDF CONVERSION FUNCTION
// =====================================
async function convertUrlToPdf() {
    const urlInput = elements.urlInput.value.trim();

    // Validation
    if (!urlInput) {
        showStatus('Please enter a URL to convert', 'error');
        elements.urlInput.focus();
        return;
    }

    if (!isValidUrl(urlInput)) {
        showStatus('Please enter a valid URL (must start with http:// or https://)', 'error');
        elements.urlInput.focus();
        return;
    }

    showLoading(true);
    showStatus('Converting web page to PDF...', 'info');

    try {
        // Send request to local Flask backend
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: urlInput,
                page_size: elements.pageSize.value,
                orientation: elements.orientation.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || response.statusText);
        }

        // Get PDF blob
        const blob = await response.blob();

        // Generate filename from URL or use custom name
        let filename = elements.fileName.value || 'webpage';
        if (!filename.endsWith('.pdf')) {
            filename += '.pdf';
        }

        // Download the PDF
        downloadBlob(blob, filename);

        showStatus(`✓ PDF generated successfully! Downloaded as "${filename}"`, 'success');

    } catch (error) {
        console.error('Conversion error:', error);
        showStatus(`✗ Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// =====================================
// EVENT LISTENERS
// =====================================
elements.convertBtn.addEventListener('click', convertUrlToPdf);

elements.clearBtn.addEventListener('click', () => {
    elements.urlInput.value = '';
    elements.urlInput.focus();
    showStatus('URL cleared', 'info');
    setTimeout(() => {
        elements.statusMessage.style.display = 'none';
    }, 2000);
});

// Quick example buttons
elements.exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const url = btn.getAttribute('data-url');
        elements.urlInput.value = url;
        elements.urlInput.focus();
        showStatus(`URL loaded: ${url}`, 'info');
        setTimeout(() => {
            elements.statusMessage.style.display = 'none';
        }, 2000);
    });
});

// Allow Enter to trigger conversion
elements.urlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        convertUrlToPdf();
    }
});

// =====================================
// INITIALIZATION
// =====================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('Web Page to PDF Converter initialized');
    elements.urlInput.focus();

    // Add welcome message
    setTimeout(() => {
        showStatus('Ready to convert! Enter a URL or try one of the examples.', 'info');
    }, 500);
});
