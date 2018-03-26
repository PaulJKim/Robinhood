/* Javascript for homepage
* Written by Paul Kim
*/

var logout = document.getElementById('logout_button');
var alphavantage_key = "SVQQFVAXS04D4RUG"

svg = d3.select("svg");
var margin = {top: 20, right: 20, bottom: 30, left: 50}

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

// console.log(positions_json);

positions_json = JSON.parse(sessionStorage.myValue);
list_of_positions = document.getElementById("list_of_positions_div");

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
	    	svg.selectAll("circle").remove();
	        get_fundamentals(this.value);
	        console.log("Getting time series data");
	        get_time_series_intraday(this.value);
	    } else {
	    	svg.selectAll("circle").remove();
	        console.log("Unselected " + this.value);
	    }
	};
}

var fundamentals_dict = {};

function get_fundamentals(ticker) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/fundamentals?ticker=" + ticker, true);
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

function get_time_series_intraday(ticker) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&outputsize=compact&apikey=" + alphavantage_key, true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
	    if (xhr.status === 200) {
	    	time_series_dict = {};
	    	time_series_dict[ticker] = JSON.parse(xhr.responseText)["Time Series (Daily)"];
	    	console.log(time_series_dict);
	    	process_time_series_data(time_series_dict, ticker);
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
	ticker = Object.keys(time_series_data)[0];
    time_series_array = [];
    for (var key in time_series_data[ticker]) {
	    if (time_series_data[ticker].hasOwnProperty(key)) {
	        time_series_array.push( [ key, time_series_data[ticker][key] ] );
	    }
	}

	var parseTime = d3.timeParse("%Y-%m-%d");

	var x = d3.scaleTime()
		.domain(d3.extent(time_series_array, function(d) {
			return parseTime(d[0]);
		}))
	    .rangeRound([margin.left, svg.attr("width") - margin.right]);

	var y = d3.scaleLinear()
		.domain(d3.extent(time_series_array, function(d) {
			return parseInt(d[1]['5. volume']);
		}))
		.range([parseInt(svg.attr("height")) + margin.top, margin.bottom]);

	var volumeline = d3.line()
	    .x(function(d) {
	    	console.log(d) 
	    	return x(parseTime(d)); })
	    .y(function(d) { 
	    	console.log(d[1]['5. volume']);
	    	return y(parseInt(d[1]['5. volume'])); });

	//console.log(time_series_array[0]);
	d3.select("svg").selectAll("path")
		.data(time_series_array)
		.enter()
		.append("path")
		.attr("class", function(d) {
			console.log(d);
			return "line";
		})
      	.attr("d", volumeline(d));
}