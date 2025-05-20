import { INode } from "./types";
import { select, zoom, forceSimulation,forceLink, forceCenter, forceManyBody, selectAll,pointer, zoomIdentity } from "d3"

// static/js/graphManager.js
export class GraphManager {

    private nodes: Map<number, INode>
    private links: Set<string>

    private width: number | undefined
    private height: number | undefined
    
    private svg: any
    private g: any
    private zoom: any
    private simulation: any
    private tooltip: any
    private colors: object | undefined

    constructor() {
        this.nodes = new Map();
        this.links = new Set();
        this.initializeD3();
        this.setupEventHandlers();
    }

    initializeD3() {
        // D3 setup
        this.width = document.getElementById('map-container')?.clientWidth;
        this.height = document.getElementById('map-container')?.clientHeight;
        
        this.svg = select("#map-container").append("svg")
            .attr("width", this.width as number)
            .attr("height", this.height as number);

        this.g = this.svg.append("g");

        this.zoom = zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            });
        
        this.svg.call(this.zoom);

        this.simulation = forceSimulation()
            .force("link", forceLink().id(d => d.id).distance(100))
            .force("charge", forceManyBody().strength(-300))
            .force("center", forceCenter(this.width as number / 2, this.height as number / 2));

        this.tooltip = select("#map-container")
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
        this.width = document.getElementById('map-container')?.clientWidth;
        this.height = document.getElementById('map-container')?.clientHeight;
        
        this.svg
            .attr("width", this.width)
            .attr("height", this.height);

        this.simulation.force("center", forceCenter(this.width as number / 2, this.height as number / 2));
        this.simulation.alpha(1).restart();
    }

    addNode(node: INode) {
        this.nodes.set(node.id, node);
    }

    addLink(source: number, target: number) {
        this.links.add(JSON.stringify({ source, target }));
    }

    getNodes() {
        return Array.from(this.nodes.values());
    }

    getLinks() {
        return Array.from(this.links).map(JSON.parse);
    }

    removeNode(id: number) {
        this.nodes.delete(id);
        this.links = new Set(
            Array.from(this.links).filter(link => {
                const { source, target } = JSON.parse(link);
                return source !== id && target !== id;
            })
        );
    }

    updateNodeLabel(id: number, label: string) {
        const node = this.nodes.get(id);
        if (node) node.label = label;
    }

    handleMouseOver(event: MouseEvent, d) {
        selectAll('.node').attr('stroke', null).attr('stroke-width', null);
        select(event.currentTarget)
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

    handleMouseOut(event: Event, d: INode) {
        select(event.currentTarget)
            .transition().duration(200)
            .attr("r", d.id === 0 ? 8 : 6)
            .attr("stroke", null)
            .attr("stroke-width", null);
        this.tooltip.style("display", "none");
    }

    handleMouseMove(event: Event) {
        const [x, y] = pointer(event, document.body);
        this.tooltip
            .style("left", (x + 15) + "px")
            .style("top", (y - 28) + "px");
    }

    centerNodeInView(d) {
        this.svg.transition()
            .duration(750)
            .call(
                this.zoom.transform,
                zoomIdentity
                    .translate(this.width as  number / 2, this.height as number / 2)
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
            .on("click", (event: Event, d: INode) => {
                if (d.id !== 0) {
                    window.dispatchEvent(new CustomEvent('nodeClick', { detail: { event, node: d } }));
                }
            })
            .on("contextmenu", (event: Event, d: INode) => {
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

    highlightNode(nodeId: number) {
        selectAll('.node').attr('stroke', null).attr('stroke-width', null);
        const node = select(`.node-${nodeId}`);
        node.attr('stroke', this.colors.highlight).attr('stroke-width', 3);

        const data = node.datum();
        this.centerNodeInView(data);
    }
}

// Make available globally
window.GraphManager = GraphManager;