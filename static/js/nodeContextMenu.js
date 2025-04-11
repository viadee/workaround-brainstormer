class NodeContextMenu{

    graphManager
    updateUIHook

    constructor(graphManager, updateUIHook){
        this.graphManager = graphManager;
        this.updateUIHook = updateUIHook;
    }

    showNodeContextMenu(event, d){
        event.preventDefault();

        this.graphManager.handleMouseOut(event, d)
        const contextMenu = document.createElement('div');
        contextMenu.style.left = event.clientX + 10 + 'px'
        contextMenu.style.top = event.clientY + 'px'
        contextMenu.className = 'node-contextmenu'
        
        const collapseNodeButton = document.createElement('button');
        collapseNodeButton.innerText = 'Collapse Node'
        collapseNodeButton.addEventListener('click', () => this.collapseNode(event, d), removeContextMenu(), {once: true})
        
        const collapseWithFeedbackButton = document.createElement('button')
        collapseWithFeedbackButton.innerText = 'Collapse with feedback'
        collapseWithFeedbackButton.addEventListener('click', () => this.handleCollapseWithFeedback())

        const expandNodeButton = document.createElement('button');
        expandNodeButton.innerText = 'Add Node'
        expandNodeButton.addEventListener('click', () => this.handleAddNode(), removeContextMenu())
        contextMenu.appendChild(collapseNodeButton);
        contextMenu.appendChild(expandNodeButton);

        contextMenu.addEventListener('mouseenter', () => contextMenu.addEventListener('mouseleave', removeContextMenu))
        document.body.addEventListener('click', removeContextMenu, {once: true}) 

        function removeContextMenu(){
            contextMenu.remove()
        }
        
        document.body.appendChild(contextMenu)
    }

    handleCollapseWithFeedback(){
          
    }
    handleAddNode(){
        const dialog = document.createElement('div')
        dialog.id = 'addnode-dialog'
        dialog.className = 'addnode-dialog'

        const textArea = document.createElement('textarea')
        textArea.classList = 'addnode-textarea'
        textArea.placeholder = 'Write workaround description...'
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
        
        function handleSubmit(){
            const textAreaEl = document.getElementById('textArea_addNode')
            if(textAreaEl == null){
                throw new Error('Textarea Element not found')
            }
            const workaroundDescription = textArea.value
            
            
            const newNode = {
                id: self.nextNodeId++,
                text: workaroundDescription,
                parent: d.id,
                expanded: false
            };
            gM.addNode(newNode);
            gM.addLink(d.id, newNode.id);
        
            d.expanded = true;
           
            self.updateUIHook();
            removeContextMenu()
            dialog.remove()
        }

        function handleClose(){
            removeContextMenu();
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
            if(parent.children == undefined || (parent.children?.length == 1 && parent.children?.find(c => c.id == d.id) != undefined )  ){
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
            d.expanded = false;
            this.updateUIHook();
            }
    }
}

window.NodeContextMenu = NodeContextMenu