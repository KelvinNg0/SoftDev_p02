var cookie_img = document.getElementById("cookie-img");
var timer = document.getElementById("timer");
var trial_type = document.getElementById("trialtype");

cookies_clicked = 0;

var scrollover = function(e) {
  var rect = e.target.getBoundingClientRect();
  if (Math.sqrt(((rect["x"] + rect["width"] / 2) - e.clientX)**2 + ((rect["y"] + rect["width"] / 2) - e.clientY)**2) <= (rect["width"] / 2)){
    e.target.style.cursor = "pointer";
    e.target.style.height= '99.95%';
    e.target.style.width= '99.95%';
    document.getElementById("filler").style.height= '29.8%';
  } else {
    e.target.style.height= '98%';
    e.target.style.width= '98%';
    e.target.style.cursor = "auto";
    document.getElementById("filler").style.height= '30%';
  }
};

var cookie_click = function(e) {
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
    data: {clicks: cookies_clicked, trial_type: trial_type.options[trial_type.selectedIndex].value},
  });
}

var start_trial = function() {
  var seconds = trial_type.options[trial_type.selectedIndex].value;
  trial_type.disabled = true;
  document.getElementById("starttimer").disabled = true;
  cookie_img.addEventListener('click', cookie_click);

  var timeInterval = setInterval(function() {
    if (seconds == 1) {
      console.log("Trial complete!");
      timer.innerHTML = 0;
      clearInterval(timeInterval);
      setTimeout(function() { alert("Trial complete! This run will be recorded."); }, 250); //otherwise the timer doesn't set to 0 until the alert is dismissed
      cookie_img.removeEventListener('click', cookie_click);
      pass_trial_data();

      //Restart
      trial_type.disabled = false;
      document.getElementById("starttimer").disabled = false;
    } else {
    --seconds;
    timer.innerHTML = seconds;
    }
  }, 1000);
}

document.getElementById("starttimer").addEventListener('click', start_trial);
cookie_img.addEventListener('mousemove', scrollover);
cookie_img.addEventListener('mouseout', scrollover);
