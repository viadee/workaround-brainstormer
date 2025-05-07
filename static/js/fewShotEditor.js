// static/js/FewShotEditor.js

class FewShotEditor {
    constructor() {
        // Initialize the examples from the server variable.
        this.allExamples = JSON.parse(JSON.stringify(defaultFewShotExamples));

        // Set the current language; default to English.
        this.currentLang = "en";
        this.modal = document.getElementById('few-shot-modal');
        this.editor = document.getElementById('few-shot-editor');
        this.feedbackMessage = document.getElementById('few-shot-feedback');
        this.langTabButtons = document.querySelectorAll('.lang-tab');

        this.initializeUIElements();
        this.setupEventListeners();
        this.populateEditor();
    }

    initializeUIElements() {
        this.editBtn = document.getElementById('edit-few-shot-btn');
        this.closeModal = this.modal.querySelector('.close-modal');
        this.addExampleBtn = document.getElementById('add-example-btn');
        this.retreiveBtn = document.getElementById('retreive-similar-few-shot-btn');
        this.description = document.getElementById('process-input');
        this.additionalContext = document.getElementById('additional-context');
        this.file_preview_img = document.getElementById('file_preview_img')
        // Populate the editor when the modal opens
        this.editBtn.addEventListener('click', () => {
            this.currentLang = "en"; // Reset to default language on open.
            this.updateLangTabs();
            this.modal.style.display = 'block';
        });
    }

    setupEventListeners() {
        this.closeModal.addEventListener('click', () => this.closeModalAndSave());
        window.addEventListener('click', (event) => {
            if (event.target === this.modal) {
                this.closeModalAndSave();
            }
        });

        this.langTabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.updateCurrentLanguageExamples(); // save current state first
                this.currentLang = btn.getAttribute('data-lang');
                this.updateLangTabs();
                this.populateEditor();
            });
        });

        this.addExampleBtn.addEventListener('click', () => {
            this.updateCurrentLanguageExamples();
            if (!this.allExamples[this.currentLang]) {
                this.allExamples[this.currentLang] = [];
            }
            this.allExamples[this.currentLang].push({ text: "", selected: true });
            this.populateEditor();
        });

        this.retreiveBtn.addEventListener('click', () => {
            this.retreiveFewShotExamples();
        });

        // Delegate removal of an example row
        this.editor.addEventListener('click', (event) => {
            if (event.target.classList.contains('remove-example-btn')) {
                const index = parseInt(event.target.getAttribute('data-index'));
                this.allExamples[this.currentLang].splice(index, 1);
                this.populateEditor();
            }
        });
    }

    updateLangTabs() {
        this.langTabButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === this.currentLang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    populateEditor() {
        this.editor.innerHTML = ''; // Clear existing rows.
        const examples = this.allExamples[this.currentLang] || [];
        examples.forEach((ex, index) => {
            const row = document.createElement('div');
            row.classList.add('few-shot-row');
            row.innerHTML = `
                <input type="checkbox" class="few-shot-checkbox" data-index="${index}" ${ex.selected ? 'checked' : ''}>
                <input type="text" class="few-shot-input" data-index="${index}" value="${ex.text}" placeholder="Enter example">
                <button type="button" class="remove-example-btn" data-index="${index}">&times;</button>
            `;
            this.editor.appendChild(row);
        });
    }

    updateCurrentLanguageExamples() {
        const rows = this.editor.querySelectorAll('.few-shot-row');
        let updated = [];
        rows.forEach((row, index) => {
            const checkbox = row.querySelector('.few-shot-checkbox');
            const inputField = row.querySelector('.few-shot-input');
            updated.push({
                text: inputField.value.trim(),
                selected: checkbox.checked
            });
        });
        this.allExamples[this.currentLang] = updated;
    }

    closeModalAndSave() {
        this.updateCurrentLanguageExamples();
        this.autoSave();
        this.modal.style.display = 'none';
    }

    autoSave() {
        const payload = {
            few_shot_examples: this.allExamples
        };
        fetch('/update_few_shot_examples', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            this.displayFeedback(data);
        })
        .catch(err => {
            console.error(err);
            this.displayError("Error saving examples.");
        });
    }

    displayFeedback(data) {
        if (data.status === 'success') {
            this.feedbackMessage.style.display = 'block';
            this.feedbackMessage.style.color = '#28a745';
            this.feedbackMessage.textContent = 'Saved successfully!';
            this.autoHideFeedback();
        } else {
            this.displayError(data.error);
        }
    }

    displayError(message) {
        this.feedbackMessage.style.display = 'block';
        this.feedbackMessage.style.color = '#dc3545';
        this.feedbackMessage.textContent = 'Error: ' + message;
    }

    autoHideFeedback() {
        setTimeout(() => {
            this.feedbackMessage.style.opacity = '0';
        }, 1500);
        setTimeout(() => {
            this.feedbackMessage.style.display = 'none';
            this.feedbackMessage.style.opacity = '1';
        }, 2000);
    }

    retreiveFewShotExamples() {
        if (!this.description.value) {
            if(this.file_preview_img.getAttribute('src') != ""){
                this.displayError('Please enter a textual process description to retrieve similar few-shot examples.')
                return;
            }
            this.displayError('Please insert a process description!');
            return;
        }
        const payload = {
            process_description: this.description.value + (this.additionalContext.value ?? "")
        };
        fetch('/retreive_similar_few_shot_examples', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.populateRetrievedExamples(data.data);
            } else {
                this.displayError(data.error);
            }
        })
        .catch(err => {
            console.error(err);
            this.displayError("Error retrieving examples.");
        });
    }

    populateRetrievedExamples(examples) {
        examples.forEach((ex, index) => {
            const row = document.createElement('div');
            row.classList.add('few-shot-row');
            row.innerHTML = `
                <input type="checkbox" class="few-shot-checkbox" data-index="${index}" checked>
                <input type="text" class="few-shot-input" data-index="${index}" value="${ex}" placeholder="Enter example">
                <button type="button" class="remove-example-btn" data-index="${index}">&times;</button>
            `;
            this.editor.appendChild(row);
        });
        this.feedbackMessage.style.display = 'block';
        this.feedbackMessage.style.color = '#28a745';
        this.feedbackMessage.textContent = 'Examples retrieved successfully!';
        this.autoHideFeedback();
    }
}

// Attach the class to the window object for global access
window.FewShotEditor = FewShotEditor;