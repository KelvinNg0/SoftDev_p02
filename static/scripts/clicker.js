var cookie_img = document.getElementById("cookie-img");
to_log = 0;
cookie_amnt = 0
var persecond_tracker = document.getElementById("persecond");
var persecond = parseFloat(persecond_tracker.innerHTML);

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

var shop = function(id) {
  $.ajax({
    url: "/shop",
    data: {id: id},
    success: function (data) {
      console.log("Perk purchased successfully.");
    }
  });
}

cookie_img.addEventListener('click', cookie_click);
cookie_img.addEventListener('mousemove', scrollover);
cookie_img.addEventListener('mouseout', scrollover);

var building_buttons = []
var cursor_button = document.getElementById("cursor_button");
cursor_button.addEventListener('click', function(e) {
  shop(0);
  persecond += 0.12; //weird float precision stuff
  persecond = Math.floor(persecond * 10) / 10;
  persecond_tracker.innerHTML = persecond;
  clearInterval(clicks_interval);
  clicks_interval = setInterval(function() {
    to_log++;
    cookie_amnt++;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
  }, 1000 / persecond);
})

var perk_0_lvl = 0
var perk_1_lvl = 0

setInterval(  function(){
    var cursor_id = 0
    var request = new XMLHttpRequest();
    request.open("GET", "/api");
    request.onload = function() {
      var data = JSON.parse(this.response);
      perk_0_lvl = data.perk_0_lvl;
      perk_1_lvl = data.perk_1_lvl;
    };
    request.send();

    /*
    //console.log(perks);
    if (perks.includes("0")){
      var new_cursor_button = cursor_button.cloneNode(true);
      new_cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor 2 [100 cookies]";
      new_cursor_button.addEventListener('click', function(e) {
        shop(1);
      });
      cursor_button.parentNode.replaceChild(new_cursor_button, cursor_button);
      cursor_button = new_cursor_button;
      cursor_id = 1
    };
    if (perks.includes("1")){
      var new_cursor_button = cursor_button.cloneNode(true);
      new_cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor 3 [250 cookies]";
      new_cursor_button.addEventListener('click', function(e) {
        shop(2);
      });
      cursor_button.parentNode.replaceChild(new_cursor_button, cursor_button);
      cursor_button = new_cursor_button;
      cursor_id = 2
    };
    if (perks.includes("2")){
      var new_cursor_button = cursor_button.cloneNode(true);
      new_cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor 4 [500 cookies]";
      new_cursor_button.addEventListener('click', function(e) {
        shop(3);
      });
      cursor_button.parentNode.replaceChild(new_cursor_button, cursor_button);
      cursor_button = new_cursor_button;
      cursor_id = 3
    };
    if (perks.includes("3")){
      var new_cursor_button = cursor_button.cloneNode(true);
      cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor 5 [1000 cookies]";
      new_cursor_button.addEventListener('click', function(e) {
        shop(3);
      });
      cursor_button.parentNode.replaceChild(new_cursor_button, cursor_button);
      cursor_button = new_cursor_button;
      cursor_id = 4
    };

*/

    pass_cookies_to_flask();
    var request = new XMLHttpRequest();
    request.open("GET", "/api/perks/" + cursor_id);
    request.onload = function() {
      //console.log(this.response);
      var data = JSON.parse(this.response);
      var price = Math.floor(data["cost"] * ((1.15) ** perk_0_lvl));
      cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor [" + price + "]";
      if (cookie_amnt < price){
        cursor_button.className = "btn btn-lg btn-secondary font-weight-bold bg-grey";
      } else{
        cursor_button.className = "btn btn-lg btn-secondary font-weight-bold bg-white";
      };
    };
    request.send();
  },
300);

var clicks_interval = setInterval(function() {
  console.log("Just need a blank interval");
}, 1000000000000)

if (persecond > 0) {
  clearInterval(clicks_interval);
  clicks_interval = setInterval(function() {
    to_log++;
    cookie_amnt++;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
  }, 1000 / persecond);
}
