function init() {

  const tabs = document.querySelectorAll('.tab');
  const pages = document.querySelectorAll('.page');

  let current = 0;

  tabs.forEach((tab, index) => {
      tab.addEventListener("click", function () {
          changeTabs(this);
          nextTab(index);
      });
  });

  function changeTabs(dot) {
      tabs.forEach(tab => {
          tab.classList.remove('active');
      });
      dot.classList.add('active');

      $("#ids").html("");
  }

  function nextTab(pageNumber) {
      const nextPage = pages[pageNumber];
      const currentPage = pages[current];

      // const nextText = nextPage.querySelector(".text");
      // const currentText = currentPage.querySelector(".text");
      const container = document.querySelector(".container");

      // const tl = new TimelineMax();
      const tl = gsap.timeline();

      tl.fromTo(currentPage, 0.3, { opacity: 1, pointerEvents: "all" }, {opacity: 0, pointerEvents: "none" })
      .fromTo(nextPage, 0.3, { opacity: 0, pointerEvents: "none" }, {opacity: 1, pointerEvents: "all" });
      // .fromTo(currentText, 0.3, { opacity: 1 }, {opacity: 0 })
      // .fromTo(nextPage, 0.3, { opacity: 0 }, {opacity: 1 });

      current = pageNumber;

  }

}

init();

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
        
        var ctx_mean = document.getElementById('g1').getContext('2d');
        $("#g1").css('background', 'white');

        var ctx_variance = document.getElementById('g2').getContext('2d');
        $("#g2").css('background', 'white');

        var ctx_qof = document.getElementById('g3').getContext('2d');
        $("#g3").css('background', 'white');

        var ctx_mean_1 = document.getElementById('g4').getContext('2d');
        $("#g4").css('background', 'white');

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

        var option_mean_1 = {
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
              var element = chart_mean_1.getElementAtEvent(evt);
              var coordinates = data_mean.datasets[0].data[element[0]._index];
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

        var chart_mean_1 = new Chart(ctx_mean_1,{
          type: 'scatter',
          data: data_mean,
          options:option_mean_1
        });
      }
    });
  }
});

$("#ids").on("click", "button.ids-agents", function() {
  Swal.fire({
    icon: "info",
    title: "Please wait",
    text: "Generating visualizer..."
  });
  $.ajax({
    url: "/",
    type: "post",
    data: {"file_location": $(this).text(), "speed": "0.5"},
    success: function(result) {
      window.swal.close();
      Swal.fire({
        icon: result.icon,
        title: result.title,
        text: result.text
      });
    }
  });
});
