const HttpHelper = require('../helpers/HttpHelper');

module.exports = {
    async getWeather(res, endpoint, city, country) {

        // *.openweathermap.org is out of scope
        let apiKey = '10a62430af617a949055a46fa6dec32f';
        let weatherData = await HttpHelper.HttpGet(`http://${endpoint}/data/2.5/weather?q=${city},${country}&units=metric&appid=${apiKey}`); 
        
        if (weatherData.name) {
            let weatherDescription = weatherData.weather[0].description;
            let weatherIcon = weatherData.weather[0].icon.slice(0, -1);
            let weatherTemp = weatherData.main.temp;

            switch (parseInt(weatherIcon)) {
                case 2: case 3: case 4:
                    weatherIcon = 'icon-clouds';
                    break;
                case 9: case 10:
                    weatherIcon = 'icon-rain';
                    break;
                case 11:
                    weatherIcon = 'icon-storm';
                    break;
                case 13:
                    weatherIcon = 'icon-snow';
                    break;
                default:
                    weatherIcon = 'icon-sun';
                    break;
            }

            return res.send({
                desc: weatherDescription,
                icon: weatherIcon,
                temp: weatherTemp,
            });
        } 

        return res.send({
            error: `Could not find ${city} or ${country}`
        });
    }
}