var cookie_img = document.getElementById("cookie-img");
to_log = 0;
cookie_amnt = 0
document.body.onload = function() {
  console.log("clicker!");
  var request = new XMLHttpRequest();
  request.open("GET", "/api");
  request.onload = function() {
    console.log(this.response);
    var data = JSON.parse(this.response);
    cookie_amnt = data.click;
    console.log(data.click);
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
  };
  request.send();
};
document.getElementById("cookie-num").innerHTML = cookie_amnt;

//(rect["x"] + rect["width"] / 2) + "," + (rect["y"] + rect["width"] / 2) + "," + (rect["width"] / 2));

var scrollover = function(e){
  var rect = e.target.getBoundingClientRect();
  if (Math.sqrt(((rect["x"] + rect["width"] / 2) - e.clientX)**2 + ((rect["y"] + rect["width"] / 2) - e.clientY)**2) <= (rect["width"] / 2)){
    e.target.style.cursor = "pointer";
    e.target.style.height= '99.95%';
    e.target.style.width= '99.95%';
    document.getElementById("filler").style.height= '29.8%';
  } else{
    e.target.style.height= '98%';
    e.target.style.width= '98%';
    e.target.style.cursor = "auto";
    document.getElementById("filler").style.height= '30%';
  };
};

var cookie_click = function(e){
  console.log("click!");
  var rect = e.target.getBoundingClientRect();
  if (Math.sqrt(((rect["x"] + rect["width"] / 2) - e.clientX)**2 + ((rect["y"] + rect["width"] / 2) - e.clientY)**2) <= (rect["width"] / 2)){
    e.target.style.height= '96%';
    e.target.style.width= '96%';
    document.getElementById("filler").style.height= '30.25%';
    setTimeout(() => {
      e.target.style.height= '99.95%';
      e.target.style.width= '99.95%';
      document.getElementById("filler").style.height= '29.8%';
    }, 150);
    to_log++;
    cookie_amnt++;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
  };
};

var pass_cookies_to_flask = function() {
  if (to_log > 0) {
    $.ajax({
      url: "/regclicks",
      data: {clicks: to_log},
      success: function (data) {
        console.log("Data received, setting current cookies to 0.");
        to_log = 0;
      }
    });
  }
}

var check_if_can_buy = function() {
  var perks = document.getElementsByClassName("shop");
  
}

cookie_img.addEventListener('click' , cookie_click);
cookie_img.addEventListener('mousemove', scrollover);
cookie_img.addEventListener('mouseout', scrollover);
setInterval(pass_cookies_to_flask, 2000);
