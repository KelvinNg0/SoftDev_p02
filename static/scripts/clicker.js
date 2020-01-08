console.log("clicker!");
var cookie_img = document.getElementById("cookie-img");
//(rect["x"] + rect["width"] / 2) + "," + (rect["y"] + rect["width"] / 2) + "," + (rect["width"] / 2));

var scrollover = function(e){
  console.log(e.target);
  var rect = e.target.getBoundingClientRect();
  //console.log(rect);
  //console.log(Math.sqrt(((rect["x"] + rect["width"] / 2) - e.clientX)**2 + ((rect["y"] + rect["width"] / 2) - e.clientY)**2));
  //console.log(rect["width"] / 2)
  if (Math.sqrt(((rect["x"] + rect["width"] / 2) - e.clientX)**2 + ((rect["y"] + rect["width"] / 2) - e.clientY)**2) <= (rect["width"] / 2)){
    e.target.style.cursor = "pointer";
    e.target.style.height= '99.75%';
    e.target.style.width= '99.75%';
    document.getElementById("filler").style.height= '29.75%';
  } else{
    e.target.style.height= '98%';
    e.target.style.width= '98%';
    e.target.style.cursor = "auto";
    document.getElementById("filler").style.height= '30%';
  };
};

cookie_img.addEventListener( 'mousemove', scrollover);
cookie_img.addEventListener( 'mouseout', scrollover);
