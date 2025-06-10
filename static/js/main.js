import FileUploadManager from "./fileUpload.js";
import FewShotEditor from "./fewShotEditor.js";
import GraphManager from "./graphManager.js";
import NodeContextMenu from "./nodeContextMenu.js";

import WorkaroundsList from "./workaroundsList.js";
import ApiService from "./apiService.js";
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
        
        this.apiService = new ApiService


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

        this.nodeContextMenu = new NodeContextMenu(this.graphManager, () => this.updateUI(), this.apiService)
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
        window.addEventListener('nodeClick', async (e) => await this.expandNode(e.detail.event, e.detail.node));
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

    processDescriptionIsDefined(){
         const description = document.getElementById('process-input').value;
         const uploadedFile = this.fileUploadManager.getUploadedFile();

         console.log
         if(!description && !uploadedFile){
            return false
         }
         return true
    }

    async createInitialStructure() {

        if(this.fetchWorkaroundsState == true){
            return;
        }

        if(!this.processDescriptionIsDefined()){
            alert("Please insert a process decription or a bpmn diagram to start the workaround generation.")
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
            this.fewShotEditor.retreiveFewShotExamples();
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
        this.apiService.setFormData(formData)
        try {
            const { roles, rolesData } = await this.expandRootNodeWithRoles(rootNode)
           
            formData.append('roles',rolesData)

            const { misfits, misfitsData } = await this.expandNodesWithMisfits(roles)

            formData.append("misfits", JSON.stringify(misfitsData))

            const {workaroundData, workarounds } = await this.expandMisfitNodesWithWorkarounds(misfits)

        } catch (error) {
            console.error('Error creating initial structure:', error);
            alert(error.message || 'Error retrieving initial workarounds.');
        } finally {
            this.spinner.style.display = "none";
            this.fetchWorkaroundsState = false
        }
    }
    

    async expandNodesWithMisfits(roles){
        const misfitData = await this.apiService.getMisfits(roles.map(roleNode => {return roleNode.label}), this.graphManager.promptExtensions.getMisfitsPromptContext())
        let misfitNodes = []
        for (const role of roles) {
                const misfits = misfitData[role.text];
                const parentNode = this.graphManager.getNodes().filter(node => node.text === role.text)[0]

                for (const misfit of misfits) {
                    const misfitNode = {
                        text:misfit.text,
                        label:misfit.label,
                        expanded:true,
                        parent:parentNode.id,
                        category:"misfit"
                    }
                    misfitNodes.push(this.graphManager.addNode(misfitNode));
                    this.graphManager.addLink(parentNode.id, misfitNode.id);
                }
                roles.expanded = true
        }

        this.updateUI();
        return { misfitsData: misfitData, misfits: misfitNodes }
    }
    async expandRootNodeWithRoles(rootNode){
        const rolesData = await this.apiService.getRoles(this.graphManager.promptExtensions.getRolesPromptContext())
        let roles = []
            rolesData.forEach(role => {
                const childNode = {
                    text:role,
                    expanded:true,
                    parent:rootNode.id,
                    category: "role",
                    label:role
                }
                roles.push(this.graphManager.addNode(childNode));
                this.graphManager.addLink(rootNode.id, childNode.id);
                rootNode.expanded = true;
            })

            this.updateUI();
            return {rolesData: rolesData, roles: roles}
    }
    async expandMisfitNodesWithWorkarounds(misfits){
        const misfitsData = {}

        for(const misfitNode of misfits){
            const parent = this.graphManager.getNodeById(misfitNode.parent)
            if(!misfitsData[parent.label]){
                misfitsData[parent.label] = []
            }
            misfitsData[parent.label].push({
                label: misfitNode.label,
                text: misfitNode.text
            })
        }

        const workaroundData = await this.apiService.getWorkarounds(misfitsData, this.graphManager.promptExtensions.getWorkaroundsPromptContext())
        let workaroundNodes = []
        for (const misfitNode of misfits) {
                const role = this.graphManager.getNodeById(misfitNode.parent)
                const workarounds = workaroundData[role.label].filter(x => x.challengeLabel === misfitNode.label)

                for (const workaround of workarounds) {
                    const workaroundNode = {
                        text: workaround.workaround,
                        expanded: false,
                        parent: misfitNode.id,
                        category: "workaround"
                    }
                    workaroundNodes.push(this.graphManager.addNode(workaroundNode));
                    this.graphManager.addLink(misfitNode.id, workaroundNode.id);
                }
                misfitNode.expanded = true;

        }
        this.updateUI()

        return { workaroundData, workarounds: workaroundNodes}
    }

    async expandWorkaroundWithWorkarounds(d){
      
        this.isExpanding = true;
        this.spinner.style.display = "block";
        let workarounds = []
            // Make the request
            const data = await this.apiService.getSimilarWorkarounds(d.text, this.graphManager.promptExtensions.getWorkaroundsPromptContext())

            // Update the graph with the response
            const { workarounds: similarWorkarounds, label: nodeLabel } = data;

            similarWorkarounds.forEach(text => {
                const childNode = {
                    text: text,
                    parent: d.id,
                    expanded: false,
                    category: "workaround"
                };
                workarounds.push(this.graphManager.addNode(childNode));
                this.graphManager.addLink(d.id, childNode.id);
            });
            this.graphManager.updateNodeLabel(d.id, nodeLabel);
            d.expanded = true
            this.updateUI();
        return {workaroundData: data, workarounds: workarounds}
    }
    // in main.js, update the expandNode method
    // only avaible for workarounds
    async expandNode(event, d) {
        if (this.isExpanding ) return;
        this.isExpanding = true;
        this.spinner.style.display = "block";
    
        switch(d.category){
            case 'root':
                await this.expandRootNodeWithRoles(d);
                this.isExpanding = false;
                this.spinner.style.display = "none";
                break;
            case 'workaround':
                await this.expandWorkaroundWithWorkarounds(d)
                this.isExpanding = false;
                this.spinner.style.display = "none";
                break;
            case 'misfit':
                await this.expandMisfitNodesWithWorkarounds([d])
                this.isExpanding = false;
                this.spinner.style.display = "none";
                break;
            case 'role':
                await this.expandNodesWithMisfits([d])
                this.isExpanding = false;
                this.spinner.style.display = "none";
                break;
            default:
                return;
        
        }
        this.isExpanding = false;
    }

    updateUI(){
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