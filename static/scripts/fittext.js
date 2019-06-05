(function(){

  var addEvent = function (el, type, fn) {
    if (el.addEventListener)
      el.addEventListener(type, fn, false);
		else
			el.attachEvent('on'+type, fn);
  };

  var extend = function(obj,ext){
    for(var key in ext)
      if(ext.hasOwnProperty(key))
        obj[key] = ext[key];
    return obj;
  };

  window.fitText = function (el, kompressor, options) {

    var settings = extend({
      'minFontSize' : -1/0,
      'maxFontSize' : 1/0
    },options);

    var fit = function (el) {
      var compressor = kompressor || 1;

      var resizer = function () {
        // el.style.fontSize = (
        //     Math.pow((1 / el.innerHTML.length) * 20000,0.4)
        // ) + 'px';
          el.style.fontSize = (1 / Math.log(Math.max(Math.min(el.clientWidth / (compressor*10),
              parseFloat(settings.maxFontSize)),
              parseFloat(settings.minFontSize))) * 50) + 'px';
        //   console.log(el.parentNode.parentNode.offsetWidth, el.parentNode.offsetHeight);
        //   if(el.parentNode.parentNode.offsetHeight < el.parentNode.offsetHeight){
        //       el.style.fontSize = el.style.fontSize / 2;
        //   }
      };

      // Call once to set.
      resizer();

      // Bind events
      // If you have any js library which support Events, replace this part
      // and remove addEvent function (or use original jQuery version)
      addEvent(window, 'resize', resizer);
      addEvent(window, 'orientationchange', resizer);
    };

    if (el.length)
      for(var i=0; i<el.length; i++)
        fit(el[i]);
    else
      fit(el);

    // return set of elements
    return el;
  };
})();