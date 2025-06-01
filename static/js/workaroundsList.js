// static/js/workaroundsList.js
class WorkaroundsList {
    constructor() {
        this.container = document.getElementById('workarounds-list');
        this.expandedNodes = new Set();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Download button handler
        document.getElementById('download-btn').addEventListener('click', (e) => {
            e.preventDefault();
            this.handleDownload();
        });
    }

    buildTreeData(nodes) {
        const nodeMap = new Map();
        nodes.forEach(n => {
            n.children = [];
            nodeMap.set(n.id, n);
        });

        let rootNode = null;
        nodes.forEach(n => {
            if (n.id === 0) {
                rootNode = n;
            } else {
                const parent = nodeMap.get(n.parent);
                if (parent) parent.children.push(n);
            }
        });
        return rootNode;
    }

    createListHtml(node) {
        const li = document.createElement('li');
        li.classList.add('workaround-item', `list-node-${node.id}`);

        const card = document.createElement('div');
        card.classList.add('workaround-card');

        const header = document.createElement('div');
        header.classList.add('card-header');

        if (node.children && node.children.length > 0) {
            const expandIcon = document.createElement('span');
            expandIcon.classList.add('expand-icon');
            expandIcon.innerHTML = '<i class="fas fa-plus-square"></i>';
            expandIcon.addEventListener('click', (evt) => {
                evt.stopPropagation();
                const isActive = li.classList.toggle('active');
                expandIcon.innerHTML = isActive
                    ? '<i class="fas fa-minus-square"></i>'
                    : '<i class="fas fa-plus-square"></i>';

                if (isActive) this.expandedNodes.add(node.id.toString());
                else this.expandedNodes.delete(node.id.toString());
            });
            header.appendChild(expandIcon);
        }

        const textSpan = document.createElement('span');
        textSpan.textContent = node.text;
        textSpan.classList.add('workaround-text');
        textSpan.addEventListener('click', () => {
            window.dispatchEvent(new CustomEvent('highlightNode', { 
                detail: { nodeId: node.id }
            }));
        });
        header.appendChild(textSpan);

        card.appendChild(header);

        if (node.children && node.children.length > 0) {
            const nestedUl = document.createElement('ul');
            nestedUl.classList.add('nested');
            node.children.forEach(child => {
                nestedUl.appendChild(this.createListHtml(child));
            });
            card.appendChild(nestedUl);
        }

        li.appendChild(card);
        return li;
    }

    updateList(nodes) {
        const scrollPosition = this.container.scrollTop;

        // Remember expansions
        Array.from(this.container.children).forEach(child => {
            const nodeClass = [...child.classList].find(cls => cls.startsWith('list-node-'));
            if (nodeClass && child.classList.contains('active')) {
                this.expandedNodes.add(nodeClass.replace('list-node-', ''));
            }
        });

        this.container.innerHTML = '';

        // Build tree
        const root = this.buildTreeData(nodes);
        if (root.children && root.children.length > 0) {
            root.children.forEach(childNode => {
                this.container.appendChild(this.createListHtml(childNode));
            });
        }

        // Restore expansions
        this.expandedNodes.forEach(id => {
            const listItem = this.container.querySelector(`.list-node-${id}`);
            if (listItem) {
                listItem.classList.add('active');
                const icon = listItem.querySelector('.expand-icon i');
                if (icon) {
                    icon.className = 'fas fa-minus-square';
                }
            }
        });

        // Keep scroll position
        this.container.scrollTop = scrollPosition;
    }

    async handleDownload() {

        const nodes = graphManager.getNodes()

        if (nodes.length == 0){
            return
        } 

        try {
            const response = await fetch('/api/update_workarounds', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    workarounds_tree: this.buildTreeData(nodes) 
                }),
            });
            
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            if (data.status === 'success') {
                window.location.href = '/download_workarounds';
            }
        } catch (error) {
            console.error('Download error:', error);
            alert('Error downloading workarounds.');
        }
    }
}

// Make available globally
window.WorkaroundsList = WorkaroundsList;