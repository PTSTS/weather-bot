
def fulfillment_response(fulfillment=None, parameters=None, session=None):
    """
    Make a JSON-like dict with the correct format for webhook
    :param fulfillment str: fulfillment message for the agent
    :param parameters dict: a dict of parameters, with key and value
    :param session: session name
    :return dict: response dict for converting to JSON
    """
    if fulfillment is not None:
        response = {
                "fulfillment_response":
                    {
                        "messages": [
                            {
                                "text": {
                                    "text": [
                                        fulfillment
                                    ]
                                }
                            }
                        ]
                    },
        }
    else:
        response = {}

    if parameters is not None:
        response['session_info'] = {
            "session": session,
            "parameters": parameters
        }

    return response
