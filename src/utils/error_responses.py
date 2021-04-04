from flask import Response
from utils.exceptions import Exception, Error


def error_bindings(e):
    if e == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value={}),
                        status=400,
                        mimetype='application/json')

    elif e == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='e',
                                                              value=None),
                        status=404,
                        mimetype='application/json')

    elif e == Error.RESOURCE_NOT_AVAILABLE:
        return Response(response=Exception.resource_not_available(property_name='e',
                                                                  value=None),
                        status=409,
                        mimetype='application/json')

    elif e == Error.CONFLICT:
        return Response(response=Exception.conflict(property_name='e',
                                                    value=None),
                        status=409,
                        mimetype='application/json')

    elif e == Error.MAX_RETRIES_EXCEEDED:
        return Response(response=Exception.max_retries_exceeded(),
                        status=500,
                        mimetype='application/json')

    elif e == Error.TOO_MANY_REQUESTS:
        return Response(response=Exception.too_many_requests(),
                        status=429,
                        mimetype='application/json')

    elif e == Error.SERVICE_UNAVAILABLE:
        return Response(response=Exception.service_unavailable(),
                        status=503,
                        mimetype='application/json')

    elif e == Error.INTERNAL_SERVICE_ERROR:
        return Response(response=Exception.internal_service_error(property_name='e',
                                                                  value='req_data'),
                        status=500,
                        mimetype='application/json')

    elif e == Error.BAD_GATEWAY:
        return Response(response=Exception.bad_gateway(),
                        status=502,
                        mimetype='application/json')

    elif e == Error.FAILED_DEPENDENCY:
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    elif e is None:
        return Response(response=Exception.error_gen(error=Error.INTERNAL_SERVICE_ERROR.name,
                                                     rel="unknown",
                                                     msg="An unknown error has occurred, returned a generic error "
                                                         "Response, check logs"))

    else:
        return None


def get_compt_error_response(e=None):
    return error_bindings(e)
