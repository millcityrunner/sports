import json
from enum import Enum, auto


def error_message_helper(msg):
    return f"{{'error': '{msg}.'}}"


def of(msg):
    return json.dumps({'error': msg})


class Error(Enum):

    #4xx
    INVALID_VALUE = auto()
    RESOURCE_NOT_FOUND = auto()
    RESOURCE_NOT_AVAILABLE = auto()
    ACTION_NOT_PERMITTED = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()
    METHOD_NOT_ALLOWED = auto()
    EMPTY_SET = auto()
    REQUEST_TIMEOUT = auto()
    CONFLICT = auto()
    TOO_MANY_REQUESTS = auto()
    FAILED_DEPENDENCY = auto()

    #5xx
    INTERNAL_SERVICE_ERROR = auto()
    BAD_GATEWAY = auto()
    SERVICE_UNAVAILABLE = auto()
    MAX_RETRIES_EXCEEDED = auto()


class Exception:
    @staticmethod
    def error_gen(error, rel, msg):
        return {
            'error': error,
            'rel': rel,
            'message': msg
        }

    @staticmethod
    def invalid_value(property_name, value, msg=None):
        error = Exception.error_gen(error=Error.INVALID_VALUE.name,
                                    rel=property_name,
                                    msg=msg)
        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def unauthorized():
        error = Exception.error_gen(error=Error.UNAUTHORIZED.name,
                                    rel="Authentication",
                                    msg="The call to the API resulted in an unauthorized response")
        return json.dumps(error)

    @staticmethod
    def forbidden():
        error = Exception.error_gen(error=Error.FORBIDDEN.name,
                                    rel="Authentication",
                                    msg="The call to the API resulted in a forbidden response")
        return json.dumps(error)

    @staticmethod
    def resource_not_found(property_name, value, msg=None):
        error = Exception.error_gen(error=Error.RESOURCE_NOT_FOUND.name,
                                    rel="Resource not found",
                                    msg=f"The resource `{property_name}` resulted in `{value}`")

        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def method_not_allowed():
        error = Exception.error_gen(error=Error.METHOD_NOT_ALLOWED.name,
                                    rel="Method not allowed",
                                    msg="The endpoint does not support the specified REST protocol")

        return json.dumps(error)

    @staticmethod
    def action_not_permitted(property_name, value, msg=None):
        # yes
        error = Exception.error_gen(error=Error.ACTION_NOT_PERMITTED.name,
                                    rel="Action not permitted",
                                    msg=f"The call to the API is not permitted for `{property_name}` with "
                                        f"value `{value}`")

        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def conflict(property_name, value, msg=None):
        error = Exception.error_gen(error=Error.CONFLICT.name,
                                    rel="Conflict",
                                    msg=f"There was a conflict attempting to process `{property_name}` with "
                                        f"value `{value}`")

        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def too_many_requests():
        error = Exception.error_gen(error=Error.TOO_MANY_REQUESTS.name,
                                    rel="Too many requests",
                                    msg="Maximum amount of calls has been reached for a given timeframe, "
                                        "please wait a few moments and try again")

        return json.dumps(error)

    @staticmethod
    def max_retries_exceeded():
        error = Exception.error_gen(error=Error.MAX_RETRIES_EXCEEDED.name,
                                    rel="Max retries exceeded",
                                    msg="Maximum retry limit reached")

        return json.dumps(error)

    @staticmethod
    def resource_not_available(property_name, value, msg=None):
        error = Exception.error_gen(error=Error.RESOURCE_NOT_AVAILABLE.name,
                                    rel="Resource not available",
                                    msg=f"The current resource `{property_name}` with value `{value}` is not "
                                        f"available at the moment")

        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def empty_set():
        error = Exception.error_gen(error=Error.EMPTY_SET.name,
                                    rel="Empty set",
                                    msg="The call resulted in an empty set, where empty set is an unexpected data type")

        return json.dumps(error)

    @staticmethod
    def failed_dependency():
        error = Exception.error_gen(error=Error.FAILED_DEPENDENCY.name,
                                    rel="Failed dependency",
                                    msg="While processing the request, there was a failed dependency on our side. "
                                        "Try again, if issue persists, contact support")

        return json.dumps(error)

    @staticmethod
    def internal_service_error(property_name, value, msg=None):
        error = Exception.error_gen(error=Error.INTERNAL_SERVICE_ERROR.name,
                                    rel="Internal service error",
                                    msg=f"The call resulted in an unexpected exception on the backend, "
                                        f"for `{property_name}` with value `{value}`")

        if msg is not None:
            error['msg'] = msg

        return json.dumps(error)

    @staticmethod
    def bad_gateway():
        error = Exception.error_gen(error=Error.BAD_GATEWAY.name,
                                    rel="Bad gateway",
                                    msg="While attempting to process the request, the call resulted in a Bad Gateway "
                                        "response")

        return json.dumps(error)

    @staticmethod
    def service_unavailable():
        error = Exception.error_gen(error=Error.SERVICE_UNAVAILABLE.name,
                                    rel="Service unavailable",
                                    msg="While attempting to process the request, the call resulted in a Service "
                                        "unavailable response")

        return json.dumps(error)

if __name__ == "__main__":
    import json
    from enum import Enum, auto


    def error_message_helper(msg):
        return f"{{'error': '{msg}.'}}"


    def of(msg):
        return json.dumps({'error': msg})


    class Error(Enum):

        # 4xx
        INVALID_VALUE = auto()
        RESOURCE_NOT_FOUND = auto()
        RESOURCE_NOT_AVAILABLE = auto()
        ACTION_NOT_PERMITTED = auto()
        UNAUTHORIZED = auto()
        FORBIDDEN = auto()
        METHOD_NOT_ALLOWED = auto()
        EMPTY_SET = auto()
        REQUEST_TIMEOUT = auto()
        CONFLICT = auto()
        TOO_MANY_REQUESTS = auto()
        FAILED_DEPENDENCY = auto()

        # 5xx
        INTERNAL_SERVICE_ERROR = auto()
        BAD_GATEWAY = auto()
        SERVICE_UNAVAILABLE = auto()
        MAX_RETRIES_EXCEEDED = auto()


    class Exception:
        @staticmethod
        def error_gen(error, rel, msg):
            return {
                'error': error,
                'rel': rel,
                'message': msg
            }

        @staticmethod
        def invalid_value(property_name, value, msg=None):
            error = Exception.error_gen(error=Error.INVALID_VALUE.name,
                                        rel=property_name,
                                        msg=msg)
            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def unauthorized():
            error = Exception.error_gen(error=Error.UNAUTHORIZED.name,
                                        rel="Authentication",
                                        msg="The call to the API resulted in an unauthorized response")
            return json.dumps(error)

        @staticmethod
        def forbidden():
            error = Exception.error_gen(error=Error.FORBIDDEN.name,
                                        rel="Authentication",
                                        msg="The call to the API resulted in a forbidden response")
            return json.dumps(error)

        @staticmethod
        def resource_not_found(property_name, value, msg=None):
            error = Exception.error_gen(error=Error.RESOURCE_NOT_FOUND.name,
                                        rel="Resource not found",
                                        msg=f"The resource `{property_name}` resulted in `{value}`")

            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def method_not_allowed():
            error = Exception.error_gen(error=Error.METHOD_NOT_ALLOWED.name,
                                        rel="Method not allowed",
                                        msg="The endpoint does not support the specified REST protocol")

            return json.dumps(error)

        @staticmethod
        def action_not_permitted(property_name, value, msg=None):
            # yes
            error = Exception.error_gen(error=Error.ACTION_NOT_PERMITTED.name,
                                        rel="Action not permitted",
                                        msg=f"The call to the API is not permitted for `{property_name}` with "
                                            f"value `{value}`")

            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def conflict(property_name, value, msg=None):
            error = Exception.error_gen(error=Error.CONFLICT.name,
                                        rel="Conflict",
                                        msg=f"There was a conflict attempting to process `{property_name}` with "
                                            f"value `{value}`")

            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def too_many_requests():
            error = Exception.error_gen(error=Error.TOO_MANY_REQUESTS.name,
                                        rel="Too many requests",
                                        msg="Maximum amount of calls has been reached for a given timeframe, "
                                            "please wait a few moments and try again")

            return json.dumps(error)

        @staticmethod
        def max_retries_exceeded():
            error = Exception.error_gen(error=Error.MAX_RETRIES_EXCEEDED.name,
                                        rel="Max retries exceeded",
                                        msg="Maximum retry limit reached")

            return json.dumps(error)

        @staticmethod
        def resource_not_available(property_name, value, msg=None):
            error = Exception.error_gen(error=Error.RESOURCE_NOT_AVAILABLE.name,
                                        rel="Resource not available",
                                        msg=f"The current resource `{property_name}` with value `{value}` is not "
                                            f"available at the moment")

            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def empty_set():
            error = Exception.error_gen(error=Error.EMPTY_SET.name,
                                        rel="Empty set",
                                        msg="The call resulted in an empty set, where empty set is an unexpected data type")

            return json.dumps(error)

        @staticmethod
        def failed_dependency():
            error = Exception.error_gen(error=Error.FAILED_DEPENDENCY.name,
                                        rel="Failed dependency",
                                        msg="While processing the request, there was a failed dependency on our side. "
                                            "Try again, if issue persists, contact support")

            return json.dumps(error)

        @staticmethod
        def internal_service_error(property_name, value, msg=None):
            error = Exception.error_gen(error=Error.INTERNAL_SERVICE_ERROR.name,
                                        rel="Internal service error",
                                        msg=f"The call resulted in an unexpected exception on the backend, "
                                            f"for `{property_name}` with value `{value}`")

            if msg is not None:
                error['msg'] = msg

            return json.dumps(error)

        @staticmethod
        def bad_gateway():
            error = Exception.error_gen(error=Error.BAD_GATEWAY.name,
                                        rel="Bad gateway",
                                        msg="While attempting to process the request, the call resulted in a Bad Gateway "
                                            "response")

            return json.dumps(error)

        @staticmethod
        def service_unavailable():
            error = Exception.error_gen(error=Error.SERVICE_UNAVAILABLE.name,
                                        rel="Service unavailable",
                                        msg="While attempting to process the request, the call resulted in a Service "
                                            "unavailable response")

            return json.dumps(error)

    for e in Error:
        print(e)