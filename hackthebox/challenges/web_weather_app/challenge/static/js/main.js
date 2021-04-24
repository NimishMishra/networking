const weather = document.getElementById('weather');

const getWeather = async () => {

    let endpoint = 'api.openweathermap.org';

    let res  = await fetch('//ip-api.com/json/')
        .catch(() => {
            weather.innerHTML = `
                <img src='/static/host-unreachable.jpg'>
                <br><br>
                <h4>👨‍🔧 Disable blocker addons</h2>
            `;
        });

    let data = await res.json();

    let { countryCode, city } = data;

    res = await fetch('/api/weather', {
        method: 'POST',
        body: JSON.stringify({
            endpoint: endpoint,
            city: city,
            country: countryCode,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    data = await res.json();

    if (data.temp) {
        weather.innerHTML = `
            <div class='${data.icon}'></div>
            <h1>City: ${city}</h1>
            <h1>Temp: ${data.temp} C</h1>
            <h3>Status: ${data.desc}</h3>
        `;
    } else {
        weather.innerHTML = `
            <h3>${data.message}</h3>
        `;
    }
};

getWeather();
setInterval(getWeather, 60 * 60 * 1000);