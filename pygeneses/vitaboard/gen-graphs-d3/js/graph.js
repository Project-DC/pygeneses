var margin = {left: 80, right: 20, top: 50, bottom: 100};

var width = 1000 - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;

var flag = true;

var t = d3.transition().duration(750);

var g = d3.select("#chart-area").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

var xAxisGroup = g.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")

var yAxisGroup = g.append("g")
  .attr("class", "y axis");

// X scale
var x = d3.scaleLinear()
  .range([0, width]);

// Y scale
var y = d3.scaleLinear()
  .range([height, 0])

// X label
g.append("text")
  .attr("y", height + 50)
  .attr("x", width / 2)
  .attr("font-size", "20px")
  .attr("text-anchor", "middle")
  .text("Time of birth");

// Y label
g.append("text")
  .attr("y", -60)
  .attr("x", -(height / 2))
  .attr("font-size", "20px")
  .attr("text-anchor", "middle")
  .attr("transform", "rotate(-90)")
  .text("Average death age")

d3.json("data/mean.json").then(data => {
  data.forEach(d => {
    d.tob = +d.tob;
    d.value = +d.value;
  });

  data.sort((x, y) => {
    return d3.ascending(x.tob, y.tob);
  });

  make_graph(data);
});

function make_graph(data) {
  var value = flag ? "value" : "value";

  x.domain([0, d3.max(data, d => {
    return d.tob;
  })]);

  y.domain([0, d3.max(data, d => {
    return d[value];
  })]);

  // X axis
  var xAxisCall = d3.axisBottom(x);
  xAxisGroup.transition(t).call(xAxisCall);

  // Y axis
  var yAxisCall = d3.axisLeft(y)
    .ticks(15);
  yAxisGroup.transition(t).call(yAxisCall);

  // JOIN new data with old elementss
  var rects = g.selectAll("circle")
    .data(data, d => {
      return d.tob;
    });

  // EXIT old elements not present in new data
  rects.exit()
    .attr("fill", "red")
  .transition(t)
    .attr("cy", y(0))
    .remove();

  // ENTER new elements present in new data.
  rects.enter()
    .append("circle")
      .attr("fill", "grey")
      .attr("cy", y(0))
      .attr("cx", d => {
        return x(d.tob);
      })
      .attr("r", 5)
      // AND UPDATE old elements present in new data
      .merge(rects)
      .transition(t)
        .attr("cx", d => {
          return x(d.tob);
        })
        .attr("cy", d => {
          return y(d[value]);
        });

}
