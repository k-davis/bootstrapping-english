<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as d3 from 'd3'
import cache from './cache.json'
import { Synset, SynsetId } from './model/Synset'

const svgRef = ref<SVGSVGElement | null>(null)

type Node = d3.SimulationNodeDatum & { id: SynsetId };
type Link = d3.SimulationLinkDatum<Node> & { source: SynsetId; target: SynsetId };

let cachedData: Map<SynsetId, Synset> | null = null;
let cacheNodes: Node[];
let cacheLinks: Link[];

onMounted(() => {
  cachedData = new Map<SynsetId, Synset>(Object.entries(cache));
 
   // Specify the dimensions of the chart.
  const width = 928;
  const height = 680;

  // The force simulation mutates links and nodes, so create a copy
  // so that re-evaluating this cell produces the same result.
  // const links = data.links.map((d: any) => ({...d}));
  // const nodes = data.nodes.map((d: any) => ({...d}));
  // just needs id
  cacheNodes = cachedData.values().toArray().map((synset: Synset) => {
    return { id: synset.synset_id };
  });

  cacheLinks = cachedData.values().toArray().flatMap((synset: Synset) => {
    const targets = Object.values(synset.definition.decomposition ?? {});
    return targets.map((target: SynsetId) => ( { source: synset.synset_id, target } as Link ));
  });

  // Create a simulation with several forces.
  const simulation = d3.forceSimulation(cacheNodes)
      // @ts-ignore
      .force("link", d3.forceLink(cacheLinks).id(node => node.id))
      .force("charge", d3.forceManyBody())
      // could set center of chart instead of providing args
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

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
      .style("stroke","none");

  // Add a line for each link, and a circle for each node.
  const link = svg.append("g")
      .attr("stroke", "#BBB")
      .attr("stroke-opacity", 1)
    .selectAll("line")
    .data(cacheLinks)
    .join("line")
      .attr("marker-end", "url(#arrowhead)")
      .attr("stroke-width", 2);

  const node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(cacheNodes)
    .join("circle")
      .attr("r", 5)
      .attr("fill", "black");

  node.append("title")
      .text(node => node.id);

  // Add a drag behavior.
  node.call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));
  
  //Set the position attributes of links and nodes each time the simulation ticks.
  simulation.on("tick", () => {
    link
        .attr("x1", link => link.source.x)
        .attr("y1", link => link.source.y)
        .attr("x2", link => link.target.x)
        .attr("y2", link => link.target.y);

        // cx and cy are the center coords of the circle svg
    node
        .attr("cx", node => node.x)
        .attr("cy", node => node.y);
    });

    // Reheat the simulation when drag starts, and fix the subject position.
  function dragstarted(event: any) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  // Update the subject (dragged node) position during drag.
  function dragged(event: any) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  // Restore the target alpha so the simulation cools after dragging ends.
  // Unfix the subject position now that it’s no longer being dragged.
  function dragended(event: any) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

});
</script>

<template>
  <main class="page">
    <h1>Word Decomposition Visualization Tool</h1>
    <svg ref="svgRef" class="chart" >
    </svg>
  </main>
</template>
