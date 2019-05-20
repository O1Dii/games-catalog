function openCloseNav() {
  let leftMenu = document.getElementById("mySidenav");

  if(leftMenu.style.width === "0px" || leftMenu.style.width === "") {
    leftMenu.style.width = "30%";
    document.getElementById("main").style.marginLeft = "15%";
    leftMenu.style.paddingLeft = "10px";
    leftMenu.style.paddingRight = "10px";
  }
  else{
    leftMenu.style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    leftMenu.style.paddingLeft = "0";
    leftMenu.style.paddingRight = "0";
  }
}

var slider = document.getElementById('slider');

noUiSlider.create(slider, {
    start: [20, 80],
    connect: true,
    range: {
        'min': 0,
        'max': 100
    }
});