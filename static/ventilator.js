function refreshCurrent()
{
    console.log('refresh current temperature');
    temperatureElement = document.getElementById('current-temperature');
    rawElement = document.getElementById('current-raw');
    percentageElement = document.getElementById('current-percentage');
    voltageElement = document.getElementById('current-voltage');
    fetch('/json/temp', { method: 'get' }).then(function(response) {
	response.json().then(function(data) {
	    temperatureElement.innerText = data.celcius;
	    rawElement.innerText = data.raw;
	    percentageElement.innerText = data.percentage;
	    voltageElement.innerText = data.volt;
	} );
    }).catch(function(err) {
	// Error :(
	temperatureElement.innerText = 'ERROR';
    });
}

function refreshState()
{
    console.log('refresh state');
    ventilatorElement = document.getElementById('state-ventilator');
    temperatureElement = document.getElementById('state-temperature');
    timeElement = document.getElementById('state-time');
    setPointElement = document.getElementById('state-set-point');

    fetch('/json/state', { method: 'get' }).then(function(response) {
	response.json().then(function(data) {
	    temperatureElement.innerText = data.celcius;
	    if ( data.on )
	    {
		ventilatorElement.innerText = 'ON';
		ventilatorElement.style = 'background-color: lightgreen;';
	    }
	    else
	    {
		ventilatorElement.innerText = 'OFF';
		ventilatorElement.style = '';
	    }
	    timeElement.innerText = data.time;
	    setPointElement.innerText = data.set_point;
	} );
    }).catch(function(err) {
	// Error :(
	ventilatorElement.innerText = 'ERROR';
	temperatureElement.innerText = 'ERROR';
	timeElement.innerText = 'ERROR';
	setPointElement.innerText = 'ERROR';
    });
}

function onLoad()
{
    if ( window.location.pathname == '/raw' )
    {
	setInterval(refreshCurrent, 3000);
    }
    else
    {
	setInterval(refreshState, 3000);
    }
}
window.onload = onLoad;
