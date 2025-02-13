// static/js/graphManager.js
class GraphManager {
    constructor() {
        this.nodes = new Map();
        this.links = new Set();
        this.initializeD3();
        this.setupEventHandlers();
    }

    initializeD3() {
        // D3 setup
        this.width = document.getElementById('map-container').clientWidth;
        this.height = document.getElementById('map-container').clientHeight;
        
        this.svg = d3.select("#map-container").append("svg")
            .attr("width", this.width)
            .attr("height", this.height);

        this.g = this.svg.append("g");

        this.zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            });
        
        this.svg.call(this.zoom);

        this.simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2));

        this.tooltip = d3.select("#map-container")
            .append("div")
            .attr("class", "node-tooltip");

        // Node colors
        this.colors = {
            root: '#ff7f0e',
            expanded: '#1f77b4',
            collapsed: '#2ca02c',
            highlight: '#ff0000',
            stroke: '#333'
        };
    }

    setupEventHandlers() {
        // Event handler bindings
        window.addEventListener('resize', () => this.handleResize());
    }

    handleResize() {
        this.width = document.getElementById('map-container').clientWidth;
        this.height = document.getElementById('map-container').clientHeight;
        
        this.svg
            .attr("width", this.width)
            .attr("height", this.height);

        this.simulation.force("center", d3.forceCenter(this.width / 2, this.height / 2));
        this.simulation.alpha(1).restart();
    }

    addNode(node) {
        this.nodes.set(node.id, node);
    }

    addLink(source, target) {
        this.links.add(JSON.stringify({ source, target }));
    }

    getNodes() {
        return Array.from(this.nodes.values());
    }

    getLinks() {
        return Array.from(this.links).map(JSON.parse);
    }

    removeNode(id) {
        this.nodes.delete(id);
        this.links = new Set(
            Array.from(this.links).filter(link => {
                const { source, target } = JSON.parse(link);
                return source !== id && target !== id;
            })
        );
    }

    updateNodeLabel(id, label) {
        const node = this.nodes.get(id);
        if (node) node.label = label;
    }

    handleMouseOver(event, d) {
        d3.selectAll('.node').attr('stroke', null).attr('stroke-width', null);
        d3.select(event.currentTarget)
            .transition().duration(200)
            .attr("r", d.id === 0 ? 12 : 10)
            .attr("stroke", this.colors.stroke)
            .attr("stroke-width", 2);

        // Show appropriate text in tooltip
        const tooltipText = d.id === 0 ? 
            (d.description || d.text) : // For root node, show description if available
            d.text; // For other nodes, show the regular text

        this.tooltip
            .html(tooltipText)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 28) + "px")
            .style("display", "block");
    }

    handleMouseOut(event, d) {
        d3.select(event.currentTarget)
            .transition().duration(200)
            .attr("r", d.id === 0 ? 8 : 6)
            .attr("stroke", null)
            .attr("stroke-width", null);
        this.tooltip.style("display", "none");
    }

    handleMouseMove(event) {
        const [x, y] = d3.pointer(event, document.body);
        this.tooltip
            .style("left", (x + 15) + "px")
            .style("top", (y - 28) + "px");
    }

    centerNodeInView(d) {
        this.svg.transition()
            .duration(750)
            .call(
                this.zoom.transform,
                d3.zoomIdentity
                    .translate(this.width / 2, this.height / 2)
                    .scale(1)
                    .translate(-d.x, -d.y)
            );
    }

    updateGraph() {
        const nodes = this.getNodes();
        const links = this.getLinks();

        // Update links
        const link = this.g.selectAll(".link")
            .data(links)
            .join("line")
            .attr("class", "link");

        // Update nodes
        const nodeGroup = this.g.selectAll(".node-group")
            .data(nodes)
            .join("g")
            .attr("class", "node-group");

        nodeGroup.selectAll("circle")
            .data(d => [d])
            .join("circle")
            .attr("class", d => `node node-${d.id}`)
            .attr("r", d => d.id === 0 ? 8 : 6)
            .attr("fill", d => {
                if (d.id === 0) return this.colors.root;
                return d.expanded ? this.colors.expanded : this.colors.collapsed;
            })
            .on("click", (event, d) => {
                if (d.id !== 0) {
                    window.dispatchEvent(new CustomEvent('nodeClick', { detail: { event, node: d } }));
                }
            })
            .on("contextmenu", (event, d) => {
                window.dispatchEvent(new CustomEvent('nodeContextMenu', { detail: { event, node: d } }));
            })
            .on("mouseover", (event, d) => this.handleMouseOver(event, d))
            .on("mouseout", (event, d) => this.handleMouseOut(event, d))
            .on("mousemove", (event) => this.handleMouseMove(event));

        nodeGroup.selectAll("text")
            .data(d => (d.expanded && d.label) ? [d] : [])
            .join("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(d => d.label)
            .attr("font-size", "10px")
            .attr("fill", "#333");

        this.simulation.nodes(nodes).on("tick", () => this.ticked(link, nodeGroup));
        this.simulation.force("link").links(links);
        this.simulation.alpha(1).restart();
    }

    ticked(link, nodeGroup) {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        nodeGroup
            .attr("transform", d => `translate(${d.x},${d.y})`);
    }

    clearGraph() {
        this.nodes.clear();
        this.links.clear();
        this.g.selectAll(".node").remove();
        this.g.selectAll(".link").remove();
    }

    highlightNode(nodeId) {
        d3.selectAll('.node').attr('stroke', null).attr('stroke-width', null);
        const node = d3.select(`.node-${nodeId}`);
        node.attr('stroke', this.colors.highlight).attr('stroke-width', 3);

        const data = node.datum();
        this.centerNodeInView(data);
    }
}

// Make available globally
window.GraphManager = GraphManager;