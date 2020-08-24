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
    $.ajax({
      url: "/",
      type: "post",
      data: {"file_location": file_location, "speed": speed},
      dataType: "json",
      success: function(result) {
        alert(result.status);
      }
    });
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

        var data_mean = {
            datasets: [{
                label: 'Average Death Age',
                backgroundColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointRadius: 10,
                pointHoverRadius: 10,
                data: JSON.parse(result.mean)
            }]
        };

        var data_variance = {
            datasets: [{
                label: 'Variance of Age',
                backgroundColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointRadius: 10,
                pointHoverRadius: 10,
                data: JSON.parse(result.variance)
            }]
        };

        var data_qof = {
            datasets: [{
                label: 'Quality of Life',
                backgroundColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointRadius: 10,
                pointHoverRadius: 10,
                data: JSON.parse(result.qof)
            }]
        };

        var option_mean = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            // onClick: function(evt) {
            //   var element = chart.getElementAtEvent(evt);
            //   var coordinates = data.datasets[0].data[element[0]._index];
            //   $.ajax({
            //     url: "/",
            //     type: "post",
            //     data: {"x": coordinates.x, "y": coordinates.y, "id": coordinates.id},
            //     dataType: "json",
            //     success: function(result) {
            //       alert("Success!");
            //     }
            //   });
            // }
        }

        var option_variance = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            // onClick: function(evt) {
            //   var element = chart.getElementAtEvent(evt);
            //   var coordinates = data.datasets[0].data[element[0]._index];
            //   $.ajax({
            //     url: "/",
            //     type: "post",
            //     data: {"x": coordinates.x, "y": coordinates.y, "id": coordinates.id},
            //     dataType: "json",
            //     success: function(result) {
            //       alert("Success!");
            //     }
            //   });
            // }
        }

        var option_qof = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            // onClick: function(evt) {
            //   var element = chart.getElementAtEvent(evt);
            //   var coordinates = data.datasets[0].data[element[0]._index];
            //   $.ajax({
            //     url: "/",
            //     type: "post",
            //     data: {"x": coordinates.x, "y": coordinates.y, "id": coordinates.id},
            //     dataType: "json",
            //     success: function(result) {
            //       alert("Success!");
            //     }
            //   });
            // }
        }

        var option_mean_1 = {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            // onClick: function(evt) {
            //   var element = chart.getElementAtEvent(evt);
            //   var coordinates = data.datasets[0].data[element[0]._index];
            //   $.ajax({
            //     url: "/",
            //     type: "post",
            //     data: {"x": coordinates.x, "y": coordinates.y, "id": coordinates.id},
            //     dataType: "json",
            //     success: function(result) {
            //       alert("Success!");
            //     }
            //   });
            // }
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

        var chart_mean = new Chart(ctx_mean_1,{
          type: 'scatter',
          data: data_mean,
          options:option_mean_1
        });
      }
    });
  }
});
