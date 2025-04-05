document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('youtube-url');
    const actionButtons = document.querySelectorAll('.action-button');
    const statusArea = document.getElementById('status-area');
    const themeToggle = document.getElementById('theme-toggle');

    // --- Form Submission Logic ---
    actionButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const url = urlInput.value.trim();
            const format = button.getAttribute('data-format');

            if (!url) {
                showStatus('Please paste a YouTube URL first.', 'error');
                urlInput.focus();
                return;
            }

            // Basic URL validation (more robust on server)
            if (!url.includes('youtube.com/') && !url.includes('youtu.be/')) {
                showStatus('Invalid YouTube URL format.', 'error');
                urlInput.focus();
                return;
            }

            // Disable buttons and show loading state
            setProcessing(true, button);
            showStatus(`Processing ${format}... Please wait. This might take a moment.`, 'loading');

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json' // Expect JSON response
                    },
                    body: JSON.stringify({ url, format })
                });

                const result = await response.json();

                if (!response.ok) {
                    // Handle HTTP errors (like 400, 429, 500)
                    throw new Error(result.error || `Server error: ${response.status}`);
                }

                // Success
                showStatus(`Success! Your ${format} is ready.`, 'success');
                addDownloadButton(result.download_url, result.filename);

            } catch (error) {
                console.error('Error:', error);
                showStatus(`Error: ${error.message || 'Could not process the request.'}`, 'error');
            } finally {
                // Re-enable buttons and remove loading state
                setProcessing(false, button);
            }
        });
    });

    // --- UI Helper Functions ---
    function showStatus(message, type = 'info') {
        statusArea.innerHTML = ''; // Clear previous messages
        const statusDiv = document.createElement('div');
        let bgColor, textColor;

        switch (type) {
            case 'error':
                bgColor = 'bg-red-100 dark:bg-red-900';
                textColor = 'text-red-700 dark:text-red-300';
                break;
            case 'success':
                bgColor = 'bg-green-100 dark:bg-green-900';
                textColor = 'text-green-700 dark:text-green-300';
                break;
            case 'loading':
                bgColor = 'bg-blue-100 dark:bg-blue-900';
                textColor = 'text-blue-700 dark:text-blue-300';
                break;
            default: // info
                bgColor = 'bg-gray-100 dark:bg-gray-700';
                textColor = 'text-gray-700 dark:text-gray-300';
        }

        statusDiv.className = `p-4 rounded-lg ${bgColor} ${textColor} transition-all duration-300`;
        statusDiv.textContent = message;
        statusArea.appendChild(statusDiv);
    }

    function addDownloadButton(url, filename) {
        // Remove previous download button if exists
        const existingButton = statusArea.querySelector('.download-link-button');
        if (existingButton) {
            existingButton.remove();
        }

        const link = document.createElement('a');
        link.href = url;
        link.textContent = `Download "${filename}"`;
        link.setAttribute('download', filename); // Suggest filename
        link.className = 'download-link-button mt-4 inline-block bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-5 rounded-lg transition duration-300 ease-in-out text-base focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800';
        link.target = '_blank'; // Open in new tab potentially, or just trigger download

         // Append the new button below the status message
        const statusDiv = statusArea.querySelector('div'); // Get the status message div
        if (statusDiv) {
            statusDiv.parentNode.insertBefore(link, statusDiv.nextSibling);
        } else {
            statusArea.appendChild(link); // Fallback if no status message div
        }

    }

    function setProcessing(isProcessing, specificButton = null) {
        actionButtons.forEach(btn => {
            btn.disabled = isProcessing;
            if (specificButton && btn === specificButton) {
                btn.classList.toggle('processing', isProcessing);
            } else if (!specificButton) { // Affect all buttons if none specified
                btn.classList.remove('processing'); // Ensure others are not stuck in processing state
            }
        });
    }

    // --- Theme Toggle ---
    function applyTheme(isDark) {
         if (isDark) {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        }
    }

    themeToggle.addEventListener('click', () => {
        const isDarkMode = document.documentElement.classList.toggle('dark');
        applyTheme(isDarkMode);
    });

    // Apply saved theme or system preference on load
    const savedTheme = localStorage.theme;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        applyTheme(true);
    } else {
         applyTheme(false); // Explicitly set light if not dark
    }

});