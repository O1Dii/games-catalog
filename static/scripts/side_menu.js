function openCloseNav() {
  let leftMenu = document.getElementById("mySidenav");

  if(leftMenu.style.width === "0px" || leftMenu.style.width === "") {
    leftMenu.style.width = "200%";
    document.getElementById("main").style.marginLeft = "15%";
    leftMenu.style.paddingLeft = "10px";
    leftMenu.style.paddingRight = "10px";
    document.getElementById("filters-title").style.display = "block";
  }
  else{
    leftMenu.style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    leftMenu.style.paddingLeft = "0";
    leftMenu.style.paddingRight = "0";
    document.getElementById("filters-title").style.display = "none";
  }
}



function getVals(){
  // Get slider values
  var parent = this.parentNode;
  var slides = parent.getElementsByTagName("input");
    var slide1 = parseFloat( slides[0].value );
    var slide2 = parseFloat( slides[1].value );
  // Neither slider will clip the other, so make sure we determine which is larger
  if( slide1 > slide2 ){ let tmp = slide2; slide2 = slide1; slide1 = tmp; }

  var displayElement = parent.getElementsByClassName("rangeValues")[0];
      displayElement.innerHTML = slide1 + " - " + slide2;
}

window.onload = function(){
  // Initialize Sliders
  var sliderSections = document.getElementsByClassName("range-slider");
      for( var x = 0; x < sliderSections.length; x++ ){
        var sliders = sliderSections[x].getElementsByTagName("input");
        for( var y = 0; y < sliders.length; y++ ){
          if( sliders[y].type ==="range" ){
            sliders[y].oninput = getVals;
            // Manually trigger event first time to display values
            sliders[y].oninput();
          }
        }
      }
}