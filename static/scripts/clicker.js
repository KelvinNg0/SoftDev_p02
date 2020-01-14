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
  var price = 0;
  if (id === 0) {
    price = perk_0_price;
    //price = perk_1_price;
  }

  $.ajax({
    url: "/shop",
    data: {id: id, price: price},
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
var grandma_button = document.getElementById("grandma_button");


var perk_0_lvl = 0
var perk_1_lvl = 0
var perk_0_price = 0

setInterval(  function(){
    var cursor_id = 0;
    var grandma_id = 1;
    var request = new XMLHttpRequest();
    request.open("GET", "/api");
    request.onload = function() {
      var data = JSON.parse(this.response);
      perk_0_lvl = data.perk_0_lvl;
      perk_1_lvl = data.perk_1_lvl;
    };
    request.send();
    pass_cookies_to_flask();
    var request = new XMLHttpRequest();
    request.open("GET", "/api/perks/" + cursor_id);
    request.onload = function() {
      //console.log(this.response);
      var data = JSON.parse(this.response);
      perk_0_price = Math.floor(data["cost"] * ((1.15) ** perk_0_lvl));
      cursor_button.innerHTML = "<img width=\"75px\" src=\"static/cursor.png\" class= \".img-fluid building-icon\">Cursor [" + perk_0_price + "]";
      if (cookie_amnt < perk_0_price){
        cursor_button.className = "btn btn-lg btn-secondary font-weight-bold bg-grey";
      } else{
        cursor_button.className = "btn btn-lg btn-secondary font-weight-bold bg-white";
      };
    };
    request.send();

    var request = new XMLHttpRequest();
    request.open("GET", "/api/perks/" + grandma_id);
    request.onload = function() {
      //console.log(this.response);
      var data = JSON.parse(this.response);
      perk_1_price = Math.floor(data["cost"] * ((1.15) ** perk_1_lvl));
      grandma_button.innerHTML = "<img width=\"75px\" src=\"static/grandma.png\" class= \".img-fluid building-icon\">Grandma [" + perk_1_price + "]";
      if (cookie_amnt < perk_1_price){
        grandma_button.className = "btn btn-lg btn-secondary font-weight-bold bg-grey";
      } else{
        grandma_button.className = "btn btn-lg btn-secondary font-weight-bold bg-white";
      };
    };
    request.send();
  },
300);

cursor_button.addEventListener('click', function(e) {
  if (cookie_amnt >= perk_0_price){
    shop(0);
    cookie_amnt -= perk_0_price;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
    //to_log -= perk_0_price; this breaks the counter, decrease cookies elsewhere
    persecond += 0.12; //weird float precision stuff
    persecond = Math.floor(persecond * 10) / 10;
    persecond_tracker.innerHTML = persecond;
    clearInterval(clicks_interval);
    clicks_interval = setInterval(function() {
      to_log++;
      cookie_amnt++;
      document.getElementById("cookie-num").innerHTML = cookie_amnt;
    }, 1000 / persecond);
  };
})

grandma_button.addEventListener('click', function(e) {
  if (cookie_amnt >= perk_1_price){
    shop(1);
    cookie_amnt -= perk_1_price;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
    //to_log -= perk_1_price; this too
    persecond += 1.02; //weird float precision stuff
    persecond = Math.floor(persecond * 10) / 10;
    persecond_tracker.innerHTML = persecond;
    clearInterval(clicks_interval);
    clicks_interval = setInterval(function() {
      to_log++;
      cookie_amnt++;
      document.getElementById("cookie-num").innerHTML = cookie_amnt;
    }, 1000 / persecond);
  };
})

var clicks_interval = setInterval(function() {
  //console.log("Just need a blank interval");
}, 1000000000000)

if (persecond > 0) {
  clearInterval(clicks_interval);
  clicks_interval = setInterval(function() {
    to_log++;
    cookie_amnt++;
    document.getElementById("cookie-num").innerHTML = cookie_amnt;
  }, 1000 / persecond);
}
