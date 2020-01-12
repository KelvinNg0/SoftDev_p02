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
var perk0 = document.getElementById("perk0");
  building_buttons.push(perk0);
var perk1 = document.getElementById("perk1");
  building_buttons.push(perk1);
var perk2 = document.getElementById("perk2");
  building_buttons.push(perk2);
var perk3 = document.getElementById("perk3");
  building_buttons.push(perk3);
var perk4 = document.getElementById("perk4");
  building_buttons.push(perk4);
perk0.addEventListener('click', function(e) {
  shop(0);
})
perk1.addEventListener('click', function(e) {
  shop(1);
})
perk2.addEventListener('click', function(e) {
  shop(2);
})
perk3.addEventListener('click', function(e) {
  shop(3);
})
perk4.addEventListener('click', function(e) {
  shop(4);
})

var perks = []
setInterval(  function(){
    var request = new XMLHttpRequest();
    request.open("GET", "/api");
    request.onload = function() {
      var data = JSON.parse(this.response);
      perks = data.perk_earned_ids;
    };
    request.send();
    console.log(perks);
    if (perks.includes("0")){
      console.log("u got a zero");
      perk0.remove();
    };
    if (perks.includes("1")){
      perk1.remove();
    };
    if (perks.includes("2")){
      perk2.remove();
    };
    if (perks.includes("3")){
      perk3.remove();
    };
    if (perks.includes("4")){
      perk4.remove();
    };
  },
300);



setInterval(pass_cookies_to_flask, 2000);
