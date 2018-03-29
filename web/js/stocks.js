
// **** Your JavaScript code goes here ****

// var scale = d3.scaleLinear();
// var svg = d3.select('svg');
// var xAxis = d3.axisBottom(scale);

// svg.append('g')
// 	.attr('class', 'x axis')
// 	.attr('transform', 'translate(80,250)')
// 	.call(xAxis);
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


// d3.json('http://127.0.0.1:5000/positions' + "fundamentals?ticker=MSFT", function(data) {
    
// });

	// X Scale
// 	var hzdExtent = d3.extent(dataset, function(d){
// 		return +d['habital_zone_distance'];
// 	});

// 	var xScale = d3.scaleLinear()
// 		.domain(hzdExtent)
// 		.range([100,500]);

// 	// Y Scale
// 	var massExtent = d3.extent(dataset, function(d){
// 		return +d['mass'];
// 	});

// 	var yScale = d3.scaleLog() 
// 		.domain(massExtent)
// 		.range([60,660]);

// 	// Radius Scale
// 	var radiusExtent = d3.extent(dataset, function(d){
// 		return +d['radius'];
// 	});

// 	var radiusScale = d3.scaleSqrt()
// 		.domain(radiusExtent)
// 		.range([0, 20]);

// 	// Color Scale
// 	var colorScale = d3.scaleQuantize()
// 		.domain(hzdExtent)
// 		.range(['#d64d3f', '#96ac3d', '#208d8d']);

// 	var p = d3.select("svg").selectAll("circle")
// 		.data(dataset)
// 		.enter()
// 		.append("circle")
// 		.attr('cx', function(d) {
// 			return xScale(d['habital_zone_distance']);
// 		})
// 		.attr('cy', function(d) {
// 			return yScale(d['mass']);
// 		})
// 		.attr('r', function(d) {
// 			return radiusScale(d['radius']);
// 		})
// 		.attr('fill', function(d) {
// 			return colorScale(d['habital_zone_distance']);
// 		})
// 		.attr('opacity', .4)
// 		.attr('stroke', 'gray');

// 	var svg = d3.select('svg');

// 	var xAxis = d3.axisBottom(xScale);
// 	svg.append('g')
// 		.attr('class', 'axis')
// 		.attr('transform', 'translate(0,700)')
// 		.call(xAxis);

// 	var yAxis = d3.axisLeft(yScale);
// 	svg.append('g')
// 		.attr('class', 'axis')
// 		.attr('transform', 'translate(55,0)')
// 		.call(yAxis);


// 	svg.append('text')
// 		.attr('class', 'label')
// 		.attr('fill', 'white')
// 		.attr('transform', 'translate(230,730)')
// 		.text('Habitable Zone Distance');

// 	svg.append('text')
// 		.attr('class', 'label')
// 		.attr('fill', 'white')
// 		.attr('transform', 'rotate(270), translate(-400,15)')
// 		.text('Planet Mass (relative to Earth)');
// });

