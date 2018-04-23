// topicgraph0.js
// basic force directed graph using d3.js
// requires d3.js v3.

var colorIdx = "ABCDE"

var color = d3.scale.category10();

var box = d3.select("#graph1");

var svg = box.append("svg")
  .attr("width", "100%")
  .attr("height", "600px");

var boxBounds = box.node().getBoundingClientRect();

var force = d3.layout.force()
  .gravity(0.05)
  .distance(50)
  .charge(-300)
  .size([boxBounds.width, boxBounds.height]);

force
  .nodes(json.nodes)
  .links(json.links)
  .start();

var link = svg.selectAll(".link")
    .data(json.links)
  .enter().append("line")
    .attr("class", "link")
    .attr("stroke", d => color(d.group))
    .attr("stroke-width", d => 1 + 2 * d.weight)
    .attr("stroke-opacity", 0.5);

var node = svg.selectAll(".node")
    .data(json.nodes)
  .enter().append("g")
    .attr("class", "node")
    .call(force.drag);

node.append("circle")
  .attr("r", d => d.root ? 30 : 5 + (d.weight * 5))
  .attr("fill", d => color(colorIdx.indexOf(d.name)))
  .attr("opacity", d => d.root ? 0.9 : 0)
  .attr("class", d => d.root ? "root" : "edge");

node.append("text")
  .attr("text-anchor", "middle")
  .style("font-size", d => (d.root ? 14 : 6 + (d.weight * 4)) + "px")
  .style("fill", d => d.root ? "#fff" : "#333")
  .style("font-weight", d => d.root ? 100 : 400)
  .attr("dy", ".35em")
  .text(d => d.root ? "Topic " + d.name : d.name);

force.on("tick", function() {
  link.attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

  node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
});