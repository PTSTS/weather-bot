# weather-bot
Weather bot webhook (mainly contains API's and location processing)

To start server:
```
python server/app.py
```

`config/config.json` must be present for the server to run. The file must contain:

```
{
    "key": "AAAAA",  // your API key
    "port": 80  // (optional) custom port number
}
```

This API key is used for www.weatherapi.com

###Essential Modules
```
weather-bot
|_config
||_config.json
|_server  # contains modules for the server
||_app.py  # server app, has endpoint /weather for the webhook
||_availability.py  # process date and location availability of the weather API
||_response.py  # formulate the response with the webhook's format
||_weather.py  # communicate with the Weather API
```
