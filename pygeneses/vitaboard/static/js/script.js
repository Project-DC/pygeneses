function init() {

  const tabs = document.querySelectorAll('.tab');
  const pages = document.querySelectorAll('.page');
  const backgrounds = [
      `radial-gradient(#2B3760, #0B1023)`,
      `radial-gradient(#4E4343, #161616)`,
      `radial-gradient(#BDC3C7, #2C3E50)`,
      `radial-gradient(#4E3022, #161616)`
  ];

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

      console.log(pageNumber);
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
