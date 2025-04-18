document.addEventListener('DOMContentLoaded', function() {
    // Initialize the examples from the server variable.
    // We make a deep copy to ensure that changes in our editor don't modify the original defaults.
    let allExamples = JSON.parse(JSON.stringify(defaultFewShotExamples));
    
    // Set the current language; default to English.
    let currentLang = "en";

    const editBtn = document.getElementById('edit-few-shot-btn');
    const modal = document.getElementById('few-shot-modal');
    const closeModal = modal.querySelector('.close-modal');
    const editor = document.getElementById('few-shot-editor');
    const addExampleBtn = document.getElementById('add-example-btn');
    const feedbackMessage = document.getElementById('few-shot-feedback');
    const langTabButtons = document.querySelectorAll('.lang-tab');
    const retreiveBtn = document.getElementById('retreive-similar-few-shot-btn')
    const description = document.getElementById('process-input')
    const additionalContext = document.getElementById('additional-context');

    // Function to update language tab appearance.
    function updateLangTabs() {
        langTabButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === currentLang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Populate the editor with rows for the current language.
    function populateEditor() {
        editor.innerHTML = ''; // Clear existing rows.
        const examples = allExamples[currentLang] || [];
        examples.forEach((ex, index) => {
            const row = document.createElement('div');
            row.classList.add('few-shot-row');
            row.innerHTML = `
                <input type="checkbox" class="few-shot-checkbox" data-index="${index}" ${ex.selected ? 'checked' : ''}>
                <input type="text" class="few-shot-input" data-index="${index}" value="${ex.text}" placeholder="Enter example">
                <button type="button" class="remove-example-btn" data-index="${index}">&times;</button>
            `;
            editor.appendChild(row);
        });
    }

    // Save current editor state into the allExamples object.
    function updateCurrentLanguageExamples() {
        const rows = editor.querySelectorAll('.few-shot-row');
        let updated = [];
        rows.forEach((row, index) => {
            const checkbox = row.querySelector('.few-shot-checkbox');
            const inputField = row.querySelector('.few-shot-input');
            updated.push({
                text: inputField.value.trim(),
                selected: checkbox.checked
            });
        });
        allExamples[currentLang] = updated;
    }

    // Auto-save: send allExamples to the backend.
    function autoSave() {
        updateCurrentLanguageExamples();
        const payload = {
            few_shot_examples: allExamples
        };

        fetch('/update_few_shot_examples', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                feedbackMessage.style.display = 'block';
                feedbackMessage.style.color = '#28a745';
                feedbackMessage.textContent = 'Saved successfully!';
                setTimeout(() => { feedbackMessage.style.opacity = '0'; }, 1500);
                setTimeout(() => {
                    feedbackMessage.style.display = 'none';
                    feedbackMessage.style.opacity = '1';
                }, 2000);
            } else {
                feedbackMessage.style.display = 'block';
                feedbackMessage.style.color = '#dc3545';
                feedbackMessage.textContent = 'Error: ' + data.error;
            }
        })
        .catch(err => {
            console.error(err);
            feedbackMessage.style.display = 'block';
            feedbackMessage.style.color = '#dc3545';
            feedbackMessage.textContent = 'Error saving examples.';
        });
    }

    // Open modal and initialize editor.
    editBtn.addEventListener('click', function() {
        currentLang = "en"; // Reset to default language on open.
        updateLangTabs();
        populateEditor();
        modal.style.display = 'block';
    });

    // Handle tab clicks for language switching.
    langTabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            updateCurrentLanguageExamples(); // save current state first
            currentLang = btn.getAttribute('data-lang');
            updateLangTabs();
            populateEditor();
        });
    });

    // Delegate removal of an example row.
    editor.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-example-btn')) {
            const index = parseInt(event.target.getAttribute('data-index'));
            allExamples[currentLang].splice(index, 1);
            populateEditor();
        }
    });

    // When adding a new example, update current state then push a new one.
    addExampleBtn.addEventListener('click', function() {
        updateCurrentLanguageExamples();
        if (!allExamples[currentLang]) {
            allExamples[currentLang] = [];
        }
        allExamples[currentLang].push({ text: "", selected: true });
        populateEditor();
    });

    // When closing the modal (by clicking the close icon or outside the modal), auto-save.
    function closeModalAndSave() {
        updateCurrentLanguageExamples();
        autoSave();
        modal.style.display = 'none';
    }
    closeModal.addEventListener('click', closeModalAndSave);
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModalAndSave();
        }
    });

    // few-shot RAG functionality
    function retreiveFewShotExamples(){

        if (!description.value) {
            feedbackMessage.style.display = 'block';
            feedbackMessage.style.color = '#Ff0000';
            feedbackMessage.textContent = 'Please insert a process description or a process image!';
            setTimeout(() => { feedbackMessage.style.opacity = '0'; }, 1500);
            setTimeout(() => {
                feedbackMessage.style.display = 'none';
                feedbackMessage.style.opacity = '1';
            }, 2000);
            
            return
        }

        const payload = {
            process_description: description.value + (additionalContext.value ?? "")
        };
        fetch('/retreive_similar_few_shot_examples', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {

                data.data.forEach((ex, index) => {
                    const row = document.createElement('div');
                    row.classList.add('few-shot-row');
                    row.innerHTML = `
                        <input type="checkbox" class="few-shot-checkbox" data-index="${index}" checked>
                        <input type="text" class="few-shot-input" data-index="${index}" value="${ex}" placeholder="Enter example">
                        <button type="button" class="remove-example-btn" data-index="${index}">&times;</button>
                    `;
                    editor.appendChild(row);
                });

                feedbackMessage.style.display = 'block';
                feedbackMessage.style.color = '#28a745';
                feedbackMessage.textContent = 'Examples retreived successfully!';
                setTimeout(() => { feedbackMessage.style.opacity = '0'; }, 1500);
                setTimeout(() => {
                    feedbackMessage.style.display = 'none';
                    feedbackMessage.style.opacity = '1';
                }, 2000);
            } else {
                feedbackMessage.style.display = 'block';
                feedbackMessage.style.color = '#dc3545';
                feedbackMessage.textContent = 'Error: ' + data.error;
            }
        })
        .catch(err => {
            console.error(err);
            feedbackMessage.style.display = 'block';
            feedbackMessage.style.color = '#dc3545';
            feedbackMessage.textContent = 'Error saving examples.';
        });
    }

    // Generate similar few shot examples and initialize the editor.
    retreiveBtn.addEventListener('click', function() {
        currentLang = "en"
        updateLangTabs()
        retreiveFewShotExamples()
    })

});