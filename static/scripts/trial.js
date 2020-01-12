var cookie_img = document.getElementById("cookie-img");
cookies_clicked = 0;
timer = document.getElementById("timer");
seconds = timer.innerHTML;

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
    cookies_clicked++;
    document.getElementById("cookie-num").innerHTML = cookies_clicked;
  };
};

var pass_trial_data = function() {
  $.ajax({
    url: "/recordtrial",
    data: {clicks: cookies_clicked},
    success: function (data) {
      console.log("Data received.");
    }
  });
}

var timerInterval = setInterval

var start_timer = function() {
  cookie_img.addEventListener('click', cookie_click);

  document.getElementById("starttimer").remove();
  var timeInterval = setInterval(function() {
    if (seconds <= 1) {
      console.log("Trial complete!");
      clearInterval(timeInterval);
      timer.innerHTML = "Trial complete! This run will be recorded.";
      cookie_img.removeEventListener('click', cookie_click);
      pass_trial_data();
    } else {
    --seconds;
    timer.innerHTML = seconds;
    }
  }, 1000);
}

//only allow this when the timer has been started
//cookie_img.addEventListener('click', cookie_click);
cookie_img.addEventListener('mousemove', scrollover);
cookie_img.addEventListener('mouseout', scrollover);

document.getElementById("starttimer").addEventListener('click', start_timer);
