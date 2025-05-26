// static/js/fileUpload.js
class FileUploadManager {
    constructor() {
        this.uploadedFile = null;
        this.initializeElements();
        this.setupEventListeners();
        this.contextHint = document.getElementById('context-hint');
        this.settingsIcon = document.getElementById('settings-icon');
        this.settingsIcon.addEventListener('click', () => {
            this.contextHint.style.display = 'none';
            this.settingsIcon.classList.remove('pulse-attention');
        });
    }

    initializeElements() {
        this.processTextarea = document.getElementById("process-input");
        this.uploadContainer = document.getElementById("upload-container");
        this.fileInput = document.getElementById("file-input");
        this.browseLink = document.getElementById("browse-link");
        this.alertContainer = document.getElementById("file-upload-alert");
        this.previewOverlay = this.uploadContainer.querySelector('.file-preview-overlay');
        this.previewImage = this.previewOverlay.querySelector('img');
        this.filename = this.previewOverlay.querySelector('.file-preview-filename');
        this.removeButton = this.previewOverlay.querySelector('.file-preview-remove');
    }

    setupEventListeners() {
        // Hide alert when user starts typing in textarea
        this.processTextarea.addEventListener("input", () => {
            this.hideAlert();
        });

        // Browse link handler
        this.browseLink.addEventListener("click", (e) => {
            e.preventDefault();
            this.fileInput.click();
        });

        // File input change handler
        this.fileInput.addEventListener("change", (e) => {
            this.handleFile(e.target.files[0]);
        });

        // Drag and drop handlers for the container
        this.uploadContainer.addEventListener("dragenter", (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadContainer.classList.add("drag-over");
        });

        this.uploadContainer.addEventListener("dragover", (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadContainer.classList.add("drag-over");
        });

        this.uploadContainer.addEventListener("dragleave", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (!this.uploadContainer.contains(e.relatedTarget)) {
                this.uploadContainer.classList.remove("drag-over");
            }
        });

        this.uploadContainer.addEventListener("drop", (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadContainer.classList.remove("drag-over");
            
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                this.handleFile(e.dataTransfer.files[0]);
            }
        });

        // Remove button handler
        this.removeButton.addEventListener('click', () => this.removeFile());
    }

    showAlert(message, isError = false) {
        this.alertContainer.textContent = message;
        this.alertContainer.className = `file-upload-alert ${isError ? 'error' : 'success'}`;
        this.alertContainer.style.display = 'block';

        // Auto-hide success messages after 3 seconds
        if (!isError) {
            setTimeout(() => {
                this.hideAlert();
            }, 3000);
        }
    }

    hideAlert() {
        this.alertContainer.style.display = 'none';
    }

    handleFile(file) {
        this.hideAlert();
        this.uploadedFile = null;
        this.previewOverlay.style.display = 'none';

        if (!file) return;

        // Define valid MIME types and their extensions
        const validTypes = {
            "image/png": ".png", 
            "image/jpeg": ".jpg",
            "application/pdf": ".pdf"
        };

        // Check if the file type is valid either by MIME type or extension
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        const isValidType = Object.values(validTypes).includes(fileExtension) || 
                          Object.keys(validTypes).includes(file.type);

        if (!isValidType) {
            this.showAlert("Please upload an PNG, JPEG, or PDF file.", true);
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            this.showAlert("File size must be less than 5MB.", true);
            return;
        }

        const expertPanel = document.getElementById('expert-panel');
            if (expertPanel.style.display === 'none' || !expertPanel.style.display) {
                // Show the hint
                this.contextHint.style.display = 'flex';
                
                // Add pulse animation to settings icon
                this.settingsIcon.classList.add('pulse-attention');
            }

        // Valid file - show preview
        this.uploadedFile = file;
        
        // Set up preview
        const reader = new FileReader();
        reader.onloadend = () => {
            this.previewImage.src = reader.result;
            this.filename.textContent = file.name;
            this.previewOverlay.style.display = 'block';
        };
        reader.readAsDataURL(file);

        this.showAlert(`File "${file.name}" uploaded successfully.`, false);

        // Dispatch event for other components with filename
        window.dispatchEvent(new CustomEvent('fileUploaded', { 
            detail: { 
                file: this.uploadedFile,
                filename: file.name 
            }
        }));
    }

    removeFile() {
        this.previewOverlay.style.display = 'none';
        this.fileInput.value = '';
        this.uploadedFile = null;
        this.contextHint.style.display = 'none';
        this.settingsIcon.classList.remove('pulse-attention');
        this.hideAlert();

        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('fileRemoved'));
    }

    getUploadedFile() {
        return this.uploadedFile;
    }
}

export default FileUploadManager;