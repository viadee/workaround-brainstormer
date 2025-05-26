class NodeContextMenu{

    graphManager
    updateUIHook
    settings

    constructor(
        graphManager, 
        updateUIHook,
        workaroundGenerationSettings){
        this.graphManager = graphManager;
        this.updateUIHook = updateUIHook;
        this.settings = workaroundGenerationSettings
    }

    showNodeContextMenu(event, d){
        event.preventDefault();

        this.graphManager.handleMouseOut(event, d)
        const contextMenu = document.createElement('div');
        contextMenu.id = "contextMenu"
        contextMenu.style.left = event.clientX + 10 + 'px'
        contextMenu.style.top = event.clientY + 'px'
        contextMenu.className = 'node-contextmenu'
        
        const collapseNodeButton = document.createElement('button');
        collapseNodeButton.innerText = 'Remove Node'
        collapseNodeButton.addEventListener('click', () => this.collapseNode(event, d), this.removeContextMenu(), {once: true})
        
        const collapseWithFeedbackButton = document.createElement('button')
        collapseWithFeedbackButton.innerText = 'Collapse with feedback'
        collapseWithFeedbackButton.addEventListener('click', () => this.handleCollapseWithFeedback())

        const expandNodeButton = document.createElement('button');
        expandNodeButton.innerText = 'Add Node'
        expandNodeButton.addEventListener('click', () => this.handleAddNode(event, d), this.removeContextMenu())
        contextMenu.appendChild(collapseNodeButton);
        contextMenu.appendChild(expandNodeButton);

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
    handleAddNode(event, d){
        const dialog = document.createElement('div')
        dialog.id = 'addnode-dialog'
        dialog.className = 'addnode-dialog'

        const textArea = document.createElement('textarea')
        textArea.classList = 'addnode-textarea'
        textArea.placeholder = 'As a [role], when [situation], I [action] to [outcome].'
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
            const workaroundDescription = textArea.value
            
            
            const newNode = {
                id: gM.getNodes().reduce((max, obj) => {
                    return obj.id > max ? obj.id : max;
                }, 0) + 1,
                text: workaroundDescription,
                parent: d.id,
                expanded: false
            };
            gM.addNode(newNode);
            gM.addLink(d.id, newNode.id);
        
            d.category = "expanded";
           
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
            this.settings.addUndesirableWorkaround(this.graphManager.getNodes().find(n => n.id == d.id))
            this.graphManager.removeNode(d.id)

            const parent = this.graphManager.getNodes().find(n => n.id == d.parent)
            if(parent == undefined){
                throw new Error("Parentnode is undefined");
            }
            if(parent.children == undefined || (parent.children?.length == 1 && parent.children?.find(c => c.id == d.id) != undefined )  ){
                parent.expanded = false
            }
            this.updateUIHook()
        // recursive remove children
        }else{
            const undesirableNodes = this.graphManager.getNodes().filter(n => n.id == d.id || n.parent == d.id)
            for(const node of undesirableNodes){
                this.settings.addUndesirableWorkaround(node)
            }
            const recursiveRemove = (nodeId) => {
                const children = this.graphManager.getNodes().filter(n => n.parent === nodeId);
                children.forEach(child => {
                    recursiveRemove(child.id);
                    this.graphManager.removeNode(child.id);
                });
            };

            recursiveRemove(d.id);
            d.expanded = false;
            this.updateUIHook();
            }
    }
}

export default NodeContextMenu;