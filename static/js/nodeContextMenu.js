import ApiService from "./apiService.js";

class NodeContextMenu{

    graphManager
    updateUIHook

    constructor(
        graphManager, 
        updateUIHook,
        apiService
    ){
        this.graphManager = graphManager;
        this.updateUIHook = updateUIHook;
        this.apiService = apiService
        this.spinner = document.getElementById("map-spinner");
    }

    showNodeContextMenu(event, d){
        event.preventDefault();

        this.graphManager.handleMouseOut(event, d)
        const contextMenu = document.createElement('div');
        contextMenu.id = "contextMenu"
        contextMenu.style.left = event.clientX + 10 + 'px'
        contextMenu.style.top = event.clientY + 'px'
        contextMenu.className = 'node-contextmenu'
        
        // Add remove node button, if not root node
        if (d.category != "root"){
            const collapseNodeButton = document.createElement('button');
            collapseNodeButton.innerText = 'Remove Node'
            collapseNodeButton.addEventListener('click', () => this.collapseNode(event, d), this.removeContextMenu(), {once: true})
            contextMenu.appendChild(collapseNodeButton);
        }

        const childNodeTypeMap = {
            root: "role",
            role: "misfit",
            misfit: "workaround",
            workaround: "workaround"
        }

        if(d.category != "expanded") {

            // Add node button with textarea overlay
            const generateOneNodeButton = document.createElement('button');
            generateOneNodeButton.innerText = `Generate 1 more ${childNodeTypeMap[d.category]}`
            generateOneNodeButton.addEventListener('click', () => this.handleAddNode(event, d, 1), this.removeContextMenu())
            contextMenu.appendChild(generateOneNodeButton);

            const generateThreeNodesButton = document.createElement('button');
            generateThreeNodesButton.innerText = `Generate 3 more ${childNodeTypeMap[d.category]}s`
            generateThreeNodesButton.addEventListener('click', () => this.handleAddNode(event, d, 3), this.removeContextMenu())
            contextMenu.appendChild(generateThreeNodesButton);

            // Add node button with textarea overlay
            if(d.category != "workaround"){
                const expandNodeButton = document.createElement('button');
                expandNodeButton.innerText = `Add ${childNodeTypeMap[d.category]} manually`
                expandNodeButton.addEventListener('click', () => this.handleAddNodeManually(event, d), this.removeContextMenu())
                contextMenu.appendChild(expandNodeButton);
            } 
            

        }

        contextMenu.addEventListener('mouseenter', () => contextMenu.addEventListener('mouseleave', this.removeContextMenu))
        document.body.addEventListener('click', this.removeContextMenu, {once: true}) 
  
        document.body.appendChild(contextMenu)
    }
    removeContextMenu(){
        const menu = document.getElementById("contextMenu")
        if(menu == null){
            return;
        }
        menu.remove()
    }

    async handleAddNode(event, d, numberOfNodes) {
        this.spinner.style.display = "block";

        try{
            if (d.category === "root") {

                const roles = await this.apiService.getRoles(this.graphManager.promptExtensions.getRolesPromptContext(), numberOfNodes);

                roles.forEach(role => {
                    const childNode = {
                        text:role,
                        expanded:true,
                        parent:d.id,
                        category: "role",
                        label:role
                    }
                    this.graphManager.addNode(childNode);
                    this.graphManager.addLink(d.id, childNode.id);
                })
            }else if (d.category === "role") {
                const misfits = await this.apiService.getMisfits([d.text], this.graphManager.promptExtensions.getMisfitsPromptContext(), numberOfNodes);
      
                misfits[d.text].forEach(misfit => {
                    const childNode = {
                        text:misfit.text,
                        expanded:true,
                        parent:d.id,
                        category: "misfit",
                        label:misfit.label
                    }
                    this.graphManager.addNode(childNode);
                    this.graphManager.addLink(d.id, childNode.id);
                })
            }else if (d.category === "misfit") {
                const role = this.graphManager.getNodeById(d.parent)
                const misfitInformation = {
                    [role.text]:{
                        misfit:d.text,
                        label:d.label,
                    }
                }
                const workaroundData = await this.apiService.getWorkarounds(misfitInformation, this.graphManager.promptExtensions.getWorkaroundsPromptContext(), numberOfNodes)

                workaroundData[role.text].forEach(workaround => {
                    const childNode = {
                        text:workaround.workaround,
                        expanded:false,
                        parent:d.id,
                        category: "workaround",
                    }
                    this.graphManager.addNode(childNode);
                    this.graphManager.addLink(d.id, childNode.id);
                })
            }else if (d.category === "workaround") {
                const workaroundData = await this.apiService.getSimilarWorkarounds(d.text, this.graphManager.promptExtensions.getWorkaroundsPromptContext(), numberOfNodes)

                workaroundData['workarounds'].forEach(workaround => {
                    const childNode = {
                        text:workaround,
                        expanded:false,
                        parent:d.id,
                        category: "workaround",
                    }
                    this.graphManager.addNode(childNode);
                    this.graphManager.addLink(d.id, childNode.id);
                })
                this.graphManager.updateNodeLabel(d.id, workaroundData['label']);
                d.expanded = true
            }

            this.updateUIHook();

            this.spinner.style.display = "none";

        } catch(error) {
            console.error('Error generating additional nodes', error)
            this.spinner.style.display = "none";
        }
    }

    handleAddNodeManually(event, d){

        let placeholder;

        if(d.category == 'root'){
            placeholder = 'Role'
        }
        if(d.category == 'role') {
            placeholder = this.apiService.language == 'en' ? `As a ${d.text}, when [situation], I [complication].` : `Als ${d.text}, wenn [Situation], habe ich [Herausforderung].`
        }
        if(d.category == 'misfit') {
            placeholder = this.apiService.language == 'en' ? `As a ${this.graphManager.getNodeById(d.parent).text}, when [${d.label}], I [adaptive action], to [outcome]` : `Als ${this.graphManager.getNodeById(d.parent).text}, wenn [${d.label}], handle ich [Aktion], um [Ergebnis] zu erreichen..`
        }

        const categoryMap = {
            root: "role",
            role: "misfit",
            misfit: "workaround",
        }

        const dialog = document.createElement('div')
        dialog.id = 'addnode-dialog'
        dialog.className = 'addnode-dialog'

        const textArea = document.createElement('textarea')
        textArea.classList = 'addnode-textarea'
        textArea.placeholder = placeholder
        textArea.id = 'textArea_addNode'
        dialog.appendChild(textArea)

        const submitButton = document.createElement('button')
        submitButton.className = 'addnode-submit-btn'
        submitButton.innerText = 'Submit'
        submitButton.addEventListener('click', handleSubmit)
        dialog.appendChild(submitButton)


        const cancelButton = document.createElement('button')
        cancelButton.className = 'addnode-cancel-btn'
        cancelButton.innerText = 'Cancel'
        cancelButton.addEventListener('click', handleClose)
        dialog.appendChild(cancelButton)

        document.body.appendChild(dialog);
        
        const gM = this.graphManager
        const self = this;
        
        function handleSubmit(){
            const textAreaEl = document.getElementById('textArea_addNode')
            if(textAreaEl == null){
                throw new Error('Textarea Element not found')
            }
            const description = textArea.value
            
            
            const newNode = {
                text: description,
                parent: d.id,
                expanded: false,
                category: categoryMap[d.category]
            };
            
            if (d.category == "root") {
                newNode["label"] = description;
            }

            gM.addNode(newNode);
            gM.addLink(d.id, newNode.id);
           
            self.updateUIHook();
            self.removeContextMenu()
            dialog.remove()
        }

        function handleClose(){
            self.removeContextMenu();
            dialog.remove();
        }

    }

    collapseNode(event, d) {
        event.preventDefault();

        // dont't allow collapsing the root node
        if(d.id == 0)
            return;
        // collapse node without children
        else if(!d.expanded){
            this.graphManager.removeNode(d.id)

            const parent = this.graphManager.getNodes().find(n => n.id == d.parent)
            if(parent == undefined){
                throw new Error("Parentnode is undefined");
            }
            if(parent.children == undefined || parent.children?.length == 0 || (parent.children?.length == 1 && parent.children?.find(c => c.id == d.id) != undefined )  ){
                parent.expanded = false
            }
            this.updateUIHook()
        // recursive remove children
        }else{
            const recursiveRemove = (nodeId) => {
                const children = this.graphManager.getNodes().filter(n => n.parent === nodeId);
                children.forEach(child => {
                    recursiveRemove(child.id);
                    this.graphManager.removeNode(child.id);
                });
            };

            recursiveRemove(d.id);
            this.graphManager.removeNode(d.id);
            this.updateUIHook();
            }
    }
}

export default NodeContextMenu;
