
// static/js/main.js
class App {
    constructor() {
        this.nextNodeId = 1;
        this.isExpanding = false;
        this.currentFilename = null;
        this.fetchWorkaroundsState = false
        this.setupComponents();
        this.setupEventListeners();
    }


    setupComponents() {
        this.graphManager = window.graphManager;
        this.fileUploadManager = window.fileUploadManager;
        this.workaroundsList = window.workaroundsList;
        this.fewShotEditor = window.fewShotEditor;
        this.workaroundGenerationSettings = window.workaroundGenerationSettings

        this.spinner = document.getElementById("map-spinner");
        
        // Expert panel toggle
        const settingsIcon = document.getElementById("settings-icon");
        const expertPanel = document.getElementById("expert-panel");
        if (settingsIcon && expertPanel) {
            settingsIcon.addEventListener("click", () => {
                expertPanel.style.display = expertPanel.style.display === 'none' || !expertPanel.style.display
                    ? 'block'
                    : 'none';
            });
        }

        this.nodeContextMenu = new window.NodeContextMenu(this.graphManager, () => this.updateUI(), this.workaroundGenerationSettings)
    }

    setupEventListeners() {
        // Start button
        const startButton = document.getElementById("start-button");
        if (startButton) {
            startButton.addEventListener("click", () => this.createInitialStructure());
        }

        // File upload event
        window.addEventListener('fileUploaded', (e) => {
            this.currentFilename = e.detail.filename;
        });

        // File removal event
        window.addEventListener('fileRemoved', () => {
            this.currentFilename = null;
        });

        // Node events
        window.addEventListener('nodeClick', (e) => this.expandNode(e.detail.event, e.detail.node));
        window.addEventListener('nodeContextMenu', (e) => this.nodeContextMenu.showNodeContextMenu(e.detail.event, e.detail.node));
        window.addEventListener('highlightNode', (e) => this.graphManager.highlightNode(e.detail.nodeId));
    }

    async createInitialStructure() {
        if(this.fetchWorkaroundsState == true){
            return;
        }
        this.fetchWorkaroundsState = true
        this.graphManager.clearGraph();
        this.spinner.style.display = "block";

        const description = document.getElementById('process-input').value;
        const additionalContext = document.getElementById('additional-context')?.value || '';

        try{
            this.fewShotEditor.currentLang = "en";
            await this.fewShotEditor.updateLangTabs();
            await this.fewShotEditor.retreiveFewShotExamples();
            await this.fewShotEditor.updateCurrentLanguageExamples();
            await this.fewShotEditor.autoSave();
        } catch (error) {
            console.error('Error loading similar few-shot examples:', error);
        }

        // Create root node with description and filename if available
        const rootNode = { 
            id: 0, 
            text: this.currentFilename || description,
            description: description, // Store original description
            expanded: false 
        };
        this.graphManager.addNode(rootNode);

        // Build FormData
        const formData = new FormData();
        formData.append('process_description', description);
        formData.append('additional_context', additionalContext);
        
        const uploadedFile = this.fileUploadManager.getUploadedFile();
        if (uploadedFile) {
            formData.append('file', uploadedFile);
        }

        try {
            const response = await fetch('/start_map', {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const workarounds = await response.json();
            if (workarounds.error) {
                throw new Error(workarounds.error);
            }
            
            workarounds.forEach(text => {
                const childNode = {
                    id: this.nextNodeId++,
                    text,
                    expanded: false,
                    parent: rootNode.id
                };
                this.graphManager.addNode(childNode);
                this.graphManager.addLink(rootNode.id, childNode.id);
            });

            this.updateUI();
        } catch (error) {
            console.error('Error creating initial structure:', error);
            alert(error.message || 'Error retrieving initial workarounds.');
        } finally {
            this.spinner.style.display = "none";
            this.fetchWorkaroundsState = false
        }
    }

    // in main.js, update the expandNode method
    async expandNode(event, d) {
        if (this.isExpanding || d.expanded || d.id === 0) return;
        this.isExpanding = true;
        this.spinner.style.display = "block";
    
        try {
            // Build data object
            const requestData = {
                process_description: document.getElementById('process-input').value,
                additional_context: this.workaroundGenerationSettings.getAdditionalPromptContext(),
                similar_workaround: d.text,
                other_workarounds: this.graphManager.getNodes()
                    .filter(n => n.id !== 0 && n.id !== d.id)
                    .map(n => n.text)
            };
    
            // Get the uploaded file if any
            const uploadedFile = this.fileUploadManager?.getUploadedFile();
    
            // Choose request configuration based on whether there's a file
            let fetchConfig;
            if (uploadedFile) {
                const formData = new FormData();
                // Add all data fields individually
                formData.append('process_description', requestData.process_description);
                formData.append('additional_context', requestData.additional_context);
                formData.append('similar_workaround', requestData.similar_workaround);
                formData.append('other_workarounds', JSON.stringify(requestData.other_workarounds));
                // Then add the file
                formData.append('file', uploadedFile);
    
                fetchConfig = {
                    method: 'POST',
                    body: formData
                };
            } else {
                fetchConfig = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                };
            }
    
            // Make the request
            const response = await fetch('/get_similar_workarounds', fetchConfig);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            // Update the graph with the response
            const { workarounds: similarWorkarounds, label: nodeLabel } = data;

            similarWorkarounds.forEach(text => {
                const childNode = {
                    id: this.nextNodeId++,
                    text: text,
                    parent: d.id,
                    expanded: false
                };
                this.graphManager.addNode(childNode);
                this.graphManager.addLink(d.id, childNode.id);
            });

            d.expanded = true;
            this.graphManager.updateNodeLabel(d.id, nodeLabel);
            this.updateUI();

        } catch (error) {
            console.error('Error in expandNode:', error);
            alert(error.message || 'Error fetching similar workarounds.');
        } finally {
            this.spinner.style.display = "none";
            this.isExpanding = false;
        }
    }

    // Add helper method to handle response
    async handleSimilarWorkaroundsResponse(data, d) {
        if (data.error) {
            throw new Error(data.error);
        }

        const { workarounds: similarWorkarounds, label: nodeLabel } = data;

        similarWorkarounds.forEach(text => {
            const childNode = {
                id: this.nextNodeId++,
                text: text,
                parent: d.id,
                expanded: false
            };
            this.graphManager.addNode(childNode);
            this.graphManager.addLink(d.id, childNode.id);
        });

        d.expanded = true;
        this.graphManager.updateNodeLabel(d.id, nodeLabel);
        this.updateUI();
    }

    updateUI() {
        this.graphManager.updateGraph();
        this.workaroundsList.updateList(this.graphManager.getNodes());
    }

    
}

// Initialize everything when the page loads
window.addEventListener('load', () => {
    console.log('Initializing components...');
    
    // Create global instances
    window.graphManager = new window.GraphManager();
    window.fileUploadManager = new window.FileUploadManager();
    window.workaroundsList = new window.WorkaroundsList();
    window.workaroundGenerationSettings = new window.WorkaroundGenerationSettings()
    window.fewShotEditor = new window.FewShotEditor();
    // Initialize the main app
    window.app = new App();
    
    console.log('Initialization complete.');
});