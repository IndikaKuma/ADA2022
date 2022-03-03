def cal_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'arg1' in request_json and 'arg2' in request_json:
        arg1 = request_json['arg1']
        arg2 = request_json['arg2']
    elif request_args and 'arg1' in request_args and 'arg2' in request_args:
        arg1 = request_args['arg1']
        arg2 = request_args['arg2']
    else:
        arg1 = 0.0
        arg2 = 0.0

    return 'Total {}!'.format(float(arg1) + float(arg2))
