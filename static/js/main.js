import FileUploadManager from "./fileUpload.js";
import FewShotEditor from "./fewShotEditor.js";
import GraphManager from "./graphManager.js";
import NodeContextMenu from "./nodeContextMenu.js";
import WorkaroundGenerationSettings from "./WorkaroundGenerationSettings.js";
import WorkaroundsList from "./workaroundsList.js";
// static/js/main.js
class App {
    constructor() {
        this.isExpanding = false;
        this.currentFilename = null;
        this.fetchWorkaroundsState = false
        this.setupComponents();
        this.setupEventListeners();
    }


    setupComponents() {
        this.graphManager = new GraphManager;
        this.fileUploadManager = new FileUploadManager;
        this.workaroundsList = new WorkaroundsList;
        this.fewShotEditor = new FewShotEditor;
        this.workaroundGenerationSettings = new WorkaroundGenerationSettings;



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

        this.nodeContextMenu = new NodeContextMenu(this.graphManager, () => this.updateUI(), this.workaroundGenerationSettings)
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

        // Sidebar toggle button
        document.getElementById('toggle-btn').addEventListener('click', function() {
            const sidebar = document.getElementById('sidebar');
            // sidebar.classList.toggle('collapsed');

            // Check if the sidebar is currently collapsed
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('hidden'); // Make it visible before expanding
                setTimeout(() => {
                    sidebar.classList.remove('collapsed'); // Remove collapsed class to reveal sidebar
                }, 10); // Short delay to allow CSS transition to kick in
            } else {
                sidebar.classList.add('collapsed'); // Add collapsed class to hide sidebar

                // After finished sliding out, make it hidden
                setTimeout(() => {
                    sidebar.classList.add('hidden'); // Then add hidden class
                }, 300); // Match the duration of the CSS transition
            }
        });
        // Sidebar toggle button
        document.getElementById('toggle-btn-sidebar').addEventListener('click', function() {
            const sidebar = document.getElementById('sidebar');
            // sidebar.classList.toggle('collapsed');

            // Check if the sidebar is currently collapsed
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('hidden'); // Make it visible before expanding
                setTimeout(() => {
                    sidebar.classList.remove('collapsed'); // Remove collapsed class to reveal sidebar
                }, 10); // Short delay to allow CSS transition to kick in
            } else {
                sidebar.classList.add('collapsed'); // Add collapsed class to hide sidebar

                // After finished sliding out, make it hidden
                setTimeout(() => {
                    sidebar.classList.add('hidden'); // Then add hidden class
                }, 300); // Match the duration of the CSS transition
            }
        });
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
            this.fewShotEditor.updateLangTabs();
            // this.fewShotEditor.retreiveFewShotExamples();
            this.fewShotEditor.updateCurrentLanguageExamples();
            this.fewShotEditor.autoSave();
        } catch (error) {
            console.error('Error loading similar few-shot examples:', error);
        }

        // Create root node with description and filename if available
        const rootNode = { 
            id: 0, 
            text: this.currentFilename || description,
            description: description, // Store original description
            expanded: false,
            category: "root"
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
            const roleResponse = await fetch('/api/generateRoles', {
                method: 'POST',
                body: formData,
            });
            
            if (!roleResponse.ok) {
                throw new Error(`HTTP error! status: ${roleResponse.status}`);
            }
            
            const roleData = await roleResponse.json();
            if (roleData.error) {
                throw new Error(roleData.error);
            }

            const roles = roleData["roles"]

            roles.forEach(role => {
                const childNode = {
                    text:role,
                    expanded:true,
                    parent:rootNode.id,
                    category: "role",
                    label:role
                }
                this.graphManager.addNode(childNode);
                this.graphManager.addLink(rootNode.id, childNode.id);
            })

            this.updateUI();

            formData.append('roles',roles)

            const misfitResponse = await fetch('/api/generateMisfits', {
                method: 'POST',
                body: formData,
            });

            if (!misfitResponse.ok) {
                throw new Error(`HTTP error! status: ${misfitResponse.status}`);
            }
            
            const misfitData = await misfitResponse.json();
            if (misfitData.error) {
                throw new Error(misfitData.error);
            }


            for (const role of roles) {
                try {
                    const misfits = misfitData[role];
                    const parentNode = this.graphManager.getNodes().filter(node => node.text === role)[0]

                    for (const misfit of misfits) {
                        const misfitNode = {
                            text:misfit.text,
                            label:misfit.label,
                            expanded:true,
                            parent:parentNode.id,
                            category:"misfit"
                        }
                        this.graphManager.addNode(misfitNode);
                        this.graphManager.addLink(parentNode.id, misfitNode.id);
                    }

                } catch (error) {
                    // Handle the error or log it
                    console.error(`Error retrieving role: ${role}`, error);
                    continue; // Only if you want to skip to the next one
                }
            }

            this.updateUI();

            formData.append("misfits", JSON.stringify(misfitData))

            const workaroundResponse = await fetch('/api/generateWorkarounds', {
                method: 'POST',
                body: formData,
            });

            if (!workaroundResponse.ok) {
                throw new Error(`HTTP error! status: ${workaroundResponse.status}`);
            }
            
            const workaroundData = await workaroundResponse.json();
            if (workaroundData.error) {
                throw new Error(workaroundData.error);
            }

            const misfitNodes = this.graphManager.getNodes().filter(x => x.category === "misfit")

            for (const misfitNode of misfitNodes) {
                try {
                    const role = this.graphManager.getNodeById(misfitNode.parent)
                    const workarounds = workaroundData[role.label].filter(x => x.challengeLabel === misfitNode.label)

                    for (const workaround of workarounds) {
                        const workaroundNode = {
                            text: workaround.workaround,
                            expanded: false,
                            parent: misfitNode.id,
                            category: "workaround"
                        }
                        this.graphManager.addNode(workaroundNode);
                        this.graphManager.addLink(misfitNode.id, workaroundNode.id);
                    }
                } catch (error) {
                    console.error(`Error retrieving workaround for misfit: ${misfitNode.label}`, error)
                    continue
                }
            }

            this.updateUI()

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
                    .filter(n => n.id !== 0 && n.id !== d.id && n.category == "workaround")
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
            const response = await fetch('/api/get_similar_workarounds', fetchConfig);

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
                    text: text,
                    parent: d.id,
                    expanded: false,
                    category: "workaround"
                };
                this.graphManager.addNode(childNode);
                this.graphManager.addLink(d.id, childNode.id);
            });

            d.category = "expanded";
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
    
    // Initialize the main app
    window.app = new App();
    
    console.log('Initialization complete.');
});