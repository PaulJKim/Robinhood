

var logout = document.getElementById('logout_button');

logout.onclick = function () {

	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/logout", true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	      alert(xhr.responseText);
	      sessionStorage.myValue = null
	      location.href = "index.html";
	    } else {
	      alert(xhr.responseText + " : " + xhr.statusText);
	    }
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(null);

};

positions_json = JSON.parse(sessionStorage.myValue);

console.log(positions_json);


positions_div = document.getElementById('list_of_positions');

d3.select(positions_div).selectAll("li")
		.data(positions_json)
		.enter()
		.append("li")
		.text(function(d) { return d });