
var login = document.getElementById('login_button');
var positions_list;

login.onclick = function () {
	login_field = document.getElementById('login_field');
	password_field = document.getElementById('password_field');

	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://127.0.0.1:5000/robinhood/login", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	      alert(xhr.responseText);
	      get_positions_list();
	    } else {
	      alert(xhr.statusText);
	    }
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	response = xhr.send(JSON.stringify({
		"user" : login_field.value,
		"pass" : password_field.value
	}));

}

function get_positions_list() {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/robinhood/positions", true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	      sessionStorage.myValue = xhr.responseText;
	      location.href = "homepage.html";
	    } else {
	      console.error(xhr.responseText + " : " + xhr.statusText);
	    }
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(null);
}