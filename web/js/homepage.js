/* Javascript for homepage
* Written by Paul Kim
*/

svg = d3.select("svg");
var margin = {top: 20, right: 20, bottom: 30, left: 50}

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1;
var yyyy = today.getFullYear();

if(dd<10) {
    dd = '0'+dd
} 

if(mm<10) {
    mm = '0'+mm
} 

var parseDate = d3.timeParse("%Y-%m-%d");
today = parseDate(yyyy + '-' + mm + '-' + dd);

var logout = document.getElementById('logout');
var dropdown = document.getElementById('dropdown_button');

dropdown.onclick = function() {
	document.getElementById("settings_dropdown").classList.toggle("show");
}

window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
    var setting_dropdown = document.getElementById("settings_dropdown");
      if (setting_dropdown.classList.contains('show')) {
        setting_dropdown.classList.remove('show');
      }
  }
}

logout.onclick = function () {

	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/robinhood/logout", true);
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

// console.log(positions_json);

positions_json = JSON.parse(sessionStorage.myValue);
list_of_positions = document.getElementById("list_of_positions_div");

// Adding checkboxes for each position owned
d3.select(list_of_positions).selectAll("div")
	.data(positions_json)
	.enter()
	.append("div")
	.append("label")
	.text(function(d) { return d })
	.append("input")
	.attr("type", "checkbox")
	.attr("class", "positions_checkbox")
	.attr("value", function(d) { return d })
	.attr("id", function(d) { return d + "_checkbox" });

// Set up listeners for checkboxes retrieves data for a security when checkbox is checked
var checkbox_list = document.getElementsByClassName("positions_checkbox");

for (var i = 0; i <  checkbox_list.length; i++) {
	console.log(checkbox_list[i].value);
	checkbox_list[i].onclick = function() {

	    if(this.checked) {
	    	svg.selectAll("path").remove();
	        get_fundamentals(this.value);
	        console.log("Getting time series data");
	        get_time_series_daily(this.value);
	    } else {
	    	svg.selectAll("path").remove();
	        console.log("Unselected " + this.value);
	    }

	};
}

var fundamentals_dict = {};

function get_fundamentals(ticker) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/robinhood/fundamentals?ticker=" + ticker, true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	    	fundamentals_dict[ticker] = JSON.parse(xhr.responseText);
	    } else {
	      	alert(xhr.responseText + " : " + xhr.statusText);
	    }
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(null);
}

function get_time_series_daily(ticker) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/alphavantage/timeseries/daily/" + ticker, true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	    	time_series_list = JSON.parse(xhr.responseText);
	    	console.log(time_series_list);
	    	process_time_series_data(time_series_list, ticker);
	    } else {
	      	alert(xhr.responseText + " : " + xhr.statusText);
	    }
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(null);
}

function process_time_series_data(time_series_data) {
	// ticker = Object.keys(time_series_data)[0];
	time_series_array = [];

    for (i = 0; i < time_series_data.length; i++) {
	    time_series_array.push({key : time_series_data[i]["date"], value : time_series_data[i]});
	}

	// Scaling methods for graphing volume vs. time
	var x = d3.scaleTime()
		.domain(d3.extent(time_series_data, function(d) {
			return parseDate(d["date"]);
		}))
	    .range([margin.left, svg.attr("width") - margin.right]);

	var y = d3.scaleLinear()
		.domain(d3.extent(time_series_data, function(d) {
			return d["high_price"];
		}))
		.range([parseInt(svg.attr("height")) - margin.bottom, margin.top]);

	// Creates a line graph of volume per day
	var volumeline = d3.line()
	    .x(function(d) {
	    	console.log(d);
	    	return x(parseDate(d.key)) })
	    .y(function(d) { 
	    	return y(parseInt(d.value["high_price"])) });

	// The data here needs to passed in as an array
	svg.append("path")
		.data([time_series_array])
		.attr("class", "line")
      	.attr("d", volumeline);
}


