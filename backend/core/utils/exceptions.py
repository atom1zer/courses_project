from rest_framework.views import exception_handler
from rest_framework.response import Response
from typing import (
    Any,
    List,
    Optional,
    Union,
)
from rest_framework.status import is_client_error
from rest_framework import (
    status,
    exceptions,
)

from .error_types import (
    ErrorType,
    Error,
    ErrorResponse,
)

from icecream import ic


def custom_exception_handler(exc, context):
    ExceptionHandler(exc, context).run()
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            "error": {
                "code": response.status_code,
                "message": "An error occurred.",
                "details": {},
            }
        }

        if isinstance(response.data, dict):
            for field, error_details in response.data.items():
                custom_response["error"]["details"][field] = (
                    error_details[0]
                    if isinstance(error_details, list)
                    else error_details
                )

        return Response(custom_response, status=response.status_code)

    # Handle unexpected exceptions (500 errors)
    else:
        custom_response = {
            "error": {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred.",
                "details": str(exc),
            }
        }
        return Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExceptionHandler:
    def __init__(
        self,
        exc,
        context,
    ):
        self.exc = exc
        self.context = context

    def run(self):
        # ic(self.exc.detail, self.exc.status_code)
        # error_type = self.get_error_type()
        errors = self.get_errors()
        # error_response = self.get_error_response(error_type, errors)

    def get_error_type(self) -> ErrorType:
        if isinstance(self.exc, exceptions.ValidationError):
            return ErrorType.VALIDATION_ERROR
        elif is_client_error(self.exc.status_code):
            return ErrorType.CLIENT_ERROR
        else:
            return ErrorType.SERVER_ERROR

    def get_errors(self) -> List[Error]:
        return flatten_errors(self.exc.detail)

    def get_error_response(
        self, error_type: ErrorType, errors: List[Error]
    ) -> ErrorResponse:
        return ErrorResponse(error_type, errors)


def flatten_errors(
    detail: Union[list, dict, exceptions.ErrorDetail],
    attr: Optional[str] = None,
    index: Optional[int] = None,
) -> List[Error]:

    # fifo = [(detail, attr, index)]
    # while fifo:
    #     detail, attr, index = fifo.pop(0)
    #     ic(detail, attr, index)

    while detail:
        ic(detail)
    # while fifo:
    #     detail, attr, index = fifo.pop(0)
    # errors = []
    # while fifo:
    #     detail, attr, index = fifo.pop(0)
    #     if not detail and detail != "":
    #         continue
    #     elif isinstance(detail, list):
    #         for item in detail:
    #             if not isinstance(item, exceptions.ErrorDetail):
    #                 index = 0 if index is None else index + 1
    #                 if attr:
    #                     new_attr = f"{attr}{standardized_errors_settings.NESTED_FIELD_SEPARATOR}{index}"
    #                 else:
    #                     new_attr = str(index)
    #                 fifo.append((item, new_attr, index))
    #             else:
    #                 fifo.append((item, attr, index))

    #     elif isinstance(detail, dict):
    #         for key, value in detail.items():
    #             if attr:
    #                 key = f"{attr}{standardized_errors_settings.NESTED_FIELD_SEPARATOR}{key}"
    #             fifo.append((value, key, None))

    #     else:
    #         errors.append(Error(detail.code, str(detail), attr))

    # return errors
