from rest_framework.views import Http404, exceptions, PermissionDenied, set_rollback, Response


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(
            {
                "detail": data,
                "status_code": exc.status_code,
            },
            status=exc.status_code,
            headers=headers,
        )

    return Response(
        {
            "status_code": 500,
            "detail": str(exc)
        },
        status=500,
        headers={},
    )
