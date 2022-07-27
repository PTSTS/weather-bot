
def fulfillment_response(fulfillment=None, parameters=None, session=None):
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
