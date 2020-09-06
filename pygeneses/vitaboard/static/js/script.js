// Create the init function
function init() {

  // Select all the nav-links
  const tabs = document.querySelectorAll('.tab');

  // Select all the pages
  const pages = document.querySelectorAll('.page');

  // Assign a page counter
  let current = 0;

  // Loop through the tabs to call the acting functions on the indices of pages
  tabs.forEach((tab, index) => {
      tab.addEventListener("click", function () {
          changeTabs(this);
          nextTab(index);
      });
  });

  // When the tab is changes in the nav bar
  function changeTabs(dot) {
      tabs.forEach(tab => {
          tab.classList.remove('active');
      });
      dot.classList.add('active');

      $("#ids").html("");
  }

  // For the content in the pages
  function nextTab(pageNumber) {
      const nextPage = pages[pageNumber];
      const currentPage = pages[current];
      const container = document.querySelector(".container");

      // Initialising the gsap object
      const tl = gsap.timeline();

      // To animate the contents of the pages according the tabs
      tl.fromTo(currentPage, 0.3, { opacity: 1, pointerEvents: "all" }, {opacity: 0, pointerEvents: "none" })
      .fromTo(nextPage, 0.3, { opacity: 0, pointerEvents: "none" }, {opacity: 1, pointerEvents: "all" });
      current = pageNumber;

  }

}

// Calling the function
init();

// For the VitaViz page
$("#pygame").click(function() {
  var file_location = $("#file_location").val();
  var speed = $("#speed").val();

  if(!file_location || !speed) {
    alert("Both fields are compulsory!");
  } else {
    Swal.fire({
      icon: "info",
      title: "Please wait",
      text: "Generating visualizer..."
    });
    $.ajax({
      url: "/",
      type: "post",
      data: {"file_location": file_location, "speed": speed},
      dataType: "json",
      success: function(result) {
        window.swal.close();
        Swal.fire({
          icon: result.icon,
          title: result.title,
          text: result.text
        });
      }
    });
  }
});

// For the VitaGroups page
// Required validations and the graph generation using Chart.js
$("#groups").click(function() {
  var location = $("#location-groups").val();

  if(!location) {
    alert("Location is required!");
  } else {
    Swal.fire({
      icon: "info",
      title: "Please wait",
      text: "Generating groups..."
    });

    $.ajax({
      url: "/groups",
      type: "post",
      data: {"location": location},
      dataType: "json",
      success: function(result) {
        window.swal.close();
        Swal.fire({
          icon: result.icon,
          title: result.title,
          text: result.text
        });

        var ctx = document.getElementById('group2d').getContext('2d');
        $("#group2").css('background', 'white');

        var color = 'rgb(255, 99, 132)';
        var radius = 7;

        var data = {
          datasets: [{
              label: 'T-SNE Embeddings',
              backgroundColor: color,
              pointBackgroundColor: color,
              pointRadius: radius,
              pointHoverRadius: radius,
              data: JSON.parse(result.coord)
          }]
        };

        var option = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                      display: true,
                      labelString: 'T-SNE-1',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: 'T-SNE-2',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }]
            },
            onClick: function(evt) {
              var element = chart.getElementAtEvent(evt);
              var coordinates = data.datasets[0].data[element[0]._index];
              var list = "<ul>";
              list += "<li><button type='button' class='ids-agents'>" + coordinates.agent + "</button></li>";
              list += "</ul>";

              $("#ids").html(list);
            }
        }

        var chart = new Chart(ctx,{
          type: 'scatter',
          data: data,
          options:option
        });
      }
    })
  }
});

// For the VitaStats page
// Required validations and the graph generation using Chart.js
$("#stats").click(function() {
  var location = $("#location").val();

  if(!location) {
    alert("Location is required!");
  } else {
    Swal.fire({
      icon: "info",
      title: "Please wait",
      text: "Generating graphs..."
    });
    $.ajax({
      url: "/stats",
      type: "post",
      data: {"location": location},
      dataType: "json",
      success: function(result) {
        window.swal.close();
        Swal.fire({
          icon: result.icon,
          title: result.title,
          text: result.text
        });

        var ctx_mean = document.getElementById('g1').getContext('2d');
        $("#g1").css('background', 'white');

        var ctx_variance = document.getElementById('g2').getContext('2d');
        $("#g2").css('background', 'white');

        var ctx_qof = document.getElementById('g3').getContext('2d');
        $("#g3").css('background', 'white');

        var color = 'rgb(255, 99, 132)';
        var radius = 7;

        var data_mean = {
            datasets: [{
                label: 'Average Death Age',
                backgroundColor: color,
                pointBackgroundColor: color,
                pointRadius: radius,
                pointHoverRadius: radius,
                data: JSON.parse(result.mean)
            }]
        };

        var data_variance = {
            datasets: [{
                label: 'Variance of Age',
                backgroundColor: color,
                pointBackgroundColor: color,
                pointRadius: radius,
                pointHoverRadius: radius,
                data: JSON.parse(result.variance)
            }]
        };

        var data_qof = {
            datasets: [{
                label: 'Quality of Life',
                backgroundColor: color,
                pointBackgroundColor: color,
                pointRadius: radius,
                pointHoverRadius: radius,
                data: JSON.parse(result.qof)
            }]
        };

        var option_mean = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                      display: true,
                      labelString: 'Time of birth (in ticks)',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: 'Average death age',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }]
            },
            onClick: function(evt) {
              var element = chart_mean.getElementAtEvent(evt);
              var coordinates = data_mean.datasets[0].data[element[0]._index];
              var list = "<ul>";
              var name = "";
              coordinates.agents.forEach(ele => {
                list += "<li><button type='button' class='ids-agents'>" + ele + "</button></li>";
              });
              list += "</ul>";

              $("#ids").html(list);
            }
        }

        var option_variance = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                      display: true,
                      labelString: 'Time of birth (in ticks)',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: 'Variance in age',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }]
            },
            onClick: function(evt) {
              var element = chart_variance.getElementAtEvent(evt);
              var coordinates = data_variance.datasets[0].data[element[0]._index];
              var list = "<ul>";
              coordinates.agents.forEach(ele => {
                list += "<li><button type='button' class='ids-agents'>" + ele + "</button></li>";
              });
              list += "</ul>";

              $("#ids").html(list);
            }
        }

        var option_qof = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                      display: true,
                      labelString: 'Time of birth (in ticks)',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: 'Quality of Life',
                      fontStyle: 'bold',
                      fontSize: 14
                    }
                }]
            },
            onClick: function(evt) {
              var element = chart_qof.getElementAtEvent(evt);
              var coordinates = data_qof.datasets[0].data[element[0]._index];
              var list = "<ul>";
              coordinates.agents.forEach(ele => {
                list += "<li><button type='button' class='ids-agents'>" + ele + "</button></li>";
              });
              list += "</ul>";

              $("#ids").html(list);
            }
        }

        var chart_mean = new Chart(ctx_mean,{
          type: 'scatter',
          data: data_mean,
          options:option_mean
        });

        var chart_variance = new Chart(ctx_variance,{
          type: 'scatter',
          data: data_variance,
          options:option_variance
        });

        var chart_qof = new Chart(ctx_qof,{
          type: 'scatter',
          data: data_qof,
          options:option_qof
        });
      }
    });
  }
});

// For the VitaLineage page
// Required validations and the graph generation using Chart.js
$("#lineage").click(function() {
  var filename = $("#filename").val();

  if(!filename) {
    alert("Filename is required!");
  } else {
    Swal.fire({
      icon: "info",
      title: "Please wait",
      text: "Generating lineage..."
    });

    $.ajax({
      url: "/lineage",
      type: "post",
      data: {"filename": filename},
      success: function(result) {
        window.swal.close();
        Swal.fire({
          icon: result.icon,
          title: result.title,
          text: result.text
        });

        if(result.icon == 'success') {
          var ancestor_list = JSON.parse(result.ancestor_list);
          var successor_list = JSON.parse(result.successor_list);

          console.log(ancestor_list);
          console.log(successor_list);

          var list = "<ul>";
          var generation_max = ancestor_list[0].level;
          ancestor_list.forEach(agent_obj => {
            list += "<li>Generation " + Math.abs(agent_obj.level - generation_max) + ": ";
            list += "<button type='button' class='ids-agents'>" + agent_obj.filename + "</button></li>";
          });

          list += "<li>Generation " + Math.abs(generation_max) + " (current): ";
          list += "<button type='button' class='ids-agents'>" + filename + "</button></li>";

          successor_list.forEach(agent_obj => {
            list += "<li>Generation " + Math.abs(agent_obj.level + generation_max) + ": ";
            list += "<button type='button' class='ids-agents'>" + agent_obj.filename + "</button></li>";
          });
          list += "</ul>";

          console.log(list);
          $("#show-lineage").html(list);
        }
      }
    });
  }
});

// For the pygame visualiser that gets activated when the graph point is clicked
function visualizer(obj) {
  Swal.fire({
    icon: "info",
    title: "Please wait",
    text: "Generating visualizer..."
  });
  $.ajax({
    url: "/",
    type: "post",
    data: {"file_location": $(obj).text(), "speed": "0.5"},
    success: function(result) {
      window.swal.close();
      Swal.fire({
        icon: result.icon,
        title: result.title,
        text: result.text
      });
    }
  });
}

// Calling the visualiser on graph point click
$("#ids").on("click", "button.ids-agents", function() {
  visualizer($(this));
});

$("#show-lineage").on("click", "button.ids-agents", function() {
  visualizer($(this));
});
