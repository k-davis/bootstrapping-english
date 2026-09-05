<template>
    <svg ref="svgRef" class="chart">
    </svg>
</template>

<script setup lang="ts">
import { watch, onMounted, Ref, ref } from 'vue'
import * as d3 from 'd3'

import cache from '../cache.json'
import { Synset } from '../model/Synset'
import type { VisualizationOptions } from '../model/VisualizationOptions'

type Node = d3.SimulationNodeDatum & { id: string, fx?: number | null; fy?: number | null };
type Link = d3.SimulationLinkDatum<Node> & { source: string; target: string };

const chartWidth = 928;
const chartHeight = 680;

let cachedData: Map<string, Synset> | null = null;
let cacheNodes: Node[];
let cacheLinks: Link[];

let synsets = ref(new Map<string, Synset>());
const selectedSynset: Ref<Synset | undefined> = defineModel('selectedSynset');
    
const svgRef = ref<SVGSVGElement | null>(null)
const simulation = ref<d3.Simulation<Node, Link> | null>(null);

const props = defineProps<{ visualizationOptions: VisualizationOptions }>();

watch(() => props.visualizationOptions.showAsHierarchy, (newShowAsHierarchy: boolean, oldShowAsHierarchy: boolean) => {
    // When the display type option changes, force the chart to adjust its forces and restart the simulation
    if (!simulation.value) return;
    if (newShowAsHierarchy !== oldShowAsHierarchy) {
        if (newShowAsHierarchy) {
            addHierarchicalSimulationForces(simulation.value);
        } else {
            addForceGraphSimulationForces(simulation.value);
        }
        simulation.value.alpha(1).restart();
    }
});

watch(() => selectedSynset.value, () => {
    // When the selected synset changes, we must manually update the node colors
    d3.select(svgRef.value)
        .selectAll<SVGCircleElement, Node>("circle")
        .attr("fill", (d: Node) => d.id === selectedSynset.value?.synset_id ? "red" : "black");
});

onMounted(() => {
    // TODO: break this apart and move it out of onMounted
    cachedData = new Map<string, Synset>(Object.entries(cache as Object));
    synsets.value = cachedData;

    cacheNodes = cachedData.values().toArray().map((synset: Synset) => {
        return { id: synset.synset_id };
    });

    cacheLinks = cachedData.values().toArray().flatMap((synset: Synset) => {
        const targets = Object.values(synset.definition.decomposition ?? {});
        return targets.map((target: string) => ({ source: synset.synset_id, target } as Link));
    });

    simulation.value = d3.forceSimulation(cacheNodes);
    addHierarchicalSimulationForces(simulation.value);

    // Create the SVG container.
    const svg = d3.select(svgRef.value);

    // Define an arrowhead svg element
    svg.append("defs").append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 13)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 4)
        .attr("markerHeight", 4)
        .attr("xoverflow", "visible")
        .append("svg:path")
        .attr("d", "M 0,-5 L 10 ,0 L 0,5")
        .attr("fill", "#BBB")
        .style("stroke", "none");

    const link = svg.append("g")
        .attr("stroke", "#BBB")
        .attr("stroke-opacity", 1)
        .selectAll("path")
        .data(cacheLinks)
        .join("path")
        .attr("fill", "none")
        .attr("stroke-width", 2)
        .attr("marker-end", "url(#arrowhead)");

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll<SVGCircleElement, Node>("circle")
        .data(cacheNodes)
        .join("circle")
        .attr("r", 5)
        .attr("fill", (datum: Node) => datum.id === selectedSynset?.value?.synset_id ? "red" : "black");

    node.append("title")
        .text(node => node.id);

    node.call(d3.drag<SVGCircleElement, Node>()
        .on("drag", dragged)
        .on("end", dragended));
    node.on("click", onclick);

    // helper to ensure source/target are node objects (forceLink will set them)
    function nodeObj(n: any) { return (typeof n === "object" ? n : cacheNodes.find(x => x.id === n)); }

    simulation.value.on("tick", () => {
        link.attr("d", (d: any) => {
            const s = nodeObj(d.source);
            const t = nodeObj(d.target);
            if (!s || !t) return "";

            // self-loop
            if (s.id === t.id) {
                const x = s.x;
                const y = s.y;
                const r = 25; // loop radius
                // cubic Bezier loop to the right of the node
                return `M ${x} ${y}
                C ${x + r} ${y - r} ${x + r} ${y + r} ${x} ${y}`;
            }

            // normal straight link
            return `M ${s.x} ${s.y} L ${t.x} ${t.y}`;
        });
        node
            .attr("cx", node => node.x!)
            .attr("cy", node => node.y!);
    });
});

function addHierarchicalSimulationForces(simulation: d3.Simulation<Node, Link>): d3.Simulation<Node, Link> {
     // 1) compute out-edges and in-degree
    const outMap = new Map<string, string[]>();
    const inDegree = new Map<string, number>();
    cacheLinks.forEach(l => {
        const s = typeof l.source === "object" ? (l.source as any).id : l.source;
        const t = typeof l.target === "object" ? (l.target as any).id : l.target;
        if (!outMap.has(s)) outMap.set(s, []);
        outMap.get(s)!.push(t);
        inDegree.set(t, (inDegree.get(t) || 0) + 1);
        if (!inDegree.has(s)) inDegree.set(s, inDegree.get(s) || 0);
    });

    // 2) find roots and BFS to assign depths
    const roots = cacheNodes.filter(n => (inDegree.get(n.id) || 0) === 0).map(n => n.id);
    const depthMap = new Map<string, number>();
    const q = [...roots];
    roots.forEach(r => depthMap.set(r, 0));
    while (q.length) {
        const u = q.shift()!;
        const d = depthMap.get(u)!;
        (outMap.get(u) || []).forEach(v => {
            if (!depthMap.has(v) || depthMap.get(v)! > d + 1) {
                depthMap.set(v, d + 1);
                q.push(v);
            }
        });
    }

    // 3) attach depth to nodes and set initial y
    const levelHeight = 90; // tweak: vertical spacing per level
    const maxDepth = Math.max(0, ...Array.from(depthMap.values()));
    cacheNodes.forEach(n => {
        (n as any).depth = depthMap.has(n.id) ? depthMap.get(n.id) : maxDepth + 1;
        (n as any).y = ((n as any).depth * levelHeight) + (Math.random() - 0.5) * 10;
    });

    simulation
        // @ts-ignore
        .force("link", d3.forceLink(cacheLinks).id((node: any) => node.id))
        .force("charge", d3.forceManyBody())
        // strong vertical gravity to place nodes by depth
        .force("y", d3.forceY((d: any) => (d.depth ?? 0) * levelHeight).strength(1))
        // mild centering horizontally
        .force("x", d3.forceX(chartWidth / 2).strength(0.05))
        .force("center", d3.forceCenter(chartWidth / 2, chartHeight / 2));

    return simulation;
}

function addForceGraphSimulationForces(simulation: d3.Simulation<Node, Link>): d3.Simulation<Node, Link> {
    // @ts-ignore
    return simulation.force("link", d3.forceLink(cacheLinks).id(node => node.id))
        .force("charge", d3.forceManyBody())
        // could set center of chart instead of providing args
        .force("center", d3.forceCenter(chartWidth / 2, chartHeight / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY());
}

// Update the subject (dragged node) position during drag.
function dragged(event: d3.D3DragEvent<SVGCircleElement, Node, any>) {
    simulation.value!.alphaTarget(0.3).restart();
    event.subject.fx = event.x;
    event.subject.fy = event.y;
}

function dragended(event: d3.D3DragEvent<SVGCircleElement, Node, any>) {
    if (!event.active) simulation.value!.alphaTarget(0);
    // halt any movement in the dragged node
    event.subject.fx = null;
    event.subject.fy = null;
}

function onclick(_: MouseEvent, datum: Node) {
    selectedSynset.value = synsets.value.get(datum.id);
}

</script>

<style lang="css" scoped>
.chart {
  width: 100%;
  height: 600px;
  display: block;
  border: 1px solid #d1d5db;
  border-radius: 12px;
}
</style>