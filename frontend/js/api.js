// ===== API BASE URL =====
const API_BASE = '';

/**
 * POST a FormData to the API and return the raw Response object.
 */
async function apiPost(endpoint, formData) {
  const res = await fetch(API_BASE + endpoint, {
    method: 'POST',
    body: formData,
  });
  return res;
}

/**
 * Show the status box with a given state ('loading' | 'success' | 'error').
 */
function showStatus(el, state, message) {
  el.className = `status-box show status-${state}`;
  el.innerHTML =
    state === 'loading'
      ? `<div class="spinner"></div><span>${message}</span>`
      : `<span>${state === 'success' ? '✓' : '✗'} ${message}</span>`;
}

/**
 * Create a download button for a Blob and trigger it.
 */
function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

/**
 * Attach drag-over / drag-leave / drop handling to an upload zone.
 */
function initUploadZone(zoneEl, fileInput, labelEl) {
  zoneEl.addEventListener('dragover', (e) => {
    e.preventDefault();
    zoneEl.classList.add('drag-over');
  });
  zoneEl.addEventListener('dragleave', () => zoneEl.classList.remove('drag-over'));
  zoneEl.addEventListener('drop', (e) => {
    e.preventDefault();
    zoneEl.classList.remove('drag-over');
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      fileInput.dispatchEvent(new Event('change'));
    }
  });
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length && labelEl) {
      labelEl.style.display = 'block';
      labelEl.textContent = `📄 ${fileInput.files[0].name}`;
    }
  });
}
