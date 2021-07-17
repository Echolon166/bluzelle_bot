def returnReqError(url, result):
    """Handler for the request errors.

    Args:
        url (str): URL which the request was made.
        result (requests.models.Response): Response of the request.
    """

    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    try:
        print(f"JSON result type: {type(result.json())}")
        print(result.json())
    except:
        pass
