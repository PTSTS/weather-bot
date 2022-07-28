
import datetime
from server.response import fulfillment_response


def check_availability(date, day_weather, session_name, location):
    if day_weather.location_found and day_weather.date_available:
        response = fulfillment_response(
            f"""You asked for the weather on {date.day}/{date.month}/{date.year} in the location:
    {day_weather.location}. \nThe lowest temperature is {day_weather.low_temp} C, the highest temperature is 
    {day_weather.high_temp} C. Is this the right location you are looking for?""",
            parameters={'location_validated': True, 'date_validated': True}, session=session_name
        )
    elif day_weather.location_found and not day_weather.date_available:
        response = fulfillment_response(
            f"""Sorry, we don't have the forecast on this day for this location, can you try a different date?""",
            parameters={'location_validated': True, 'date_validated': False, 'date': None}, session=session_name
        )
    elif not day_weather.location_found:
        response = fulfillment_response(
            f"""We couldn't find this location "{location}".""",
            parameters={'location_validated': False, 'location': None}, session=session_name
        )
    else:
        response = fulfillment_response(
            f"""Sorry, something went wrong. {day_weather.error_message}.""",
            parameters={'location_validated': False}, session=session_name
        )
    return response


def check_date(date, session_name):
    print('Checking date')
    current_date = datetime.date.today()
    if date - current_date > datetime.timedelta(days=10):
        response = fulfillment_response(
            """Sorry, we can only provide forecast for the next 10 days.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    elif date < datetime.date.today() - datetime.timedelta(days=1):
        response = fulfillment_response(
            """Sorry, we don't have record for historical weather.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    else:
        response = fulfillment_response(parameters={'date_validated': True}, session=session_name)
    return response
