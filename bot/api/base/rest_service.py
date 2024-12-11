from decimal import *
from pprint import pprint
from typing import Generic, Type, Any
from timeit import default_timer as timer

import pybit
from pydantic import ValidationError
from pybit.unified_trading import HTTP

from utils.logger import log
from api.utils.const import MODEL
from api.utils.const import RESP, REQ
from utils.classifiers import ServiceStatus
from api.base.model.request import RequestParams
from api.base.model.response import ServiceResponse, ErrorResponseData
from api.utils.service_exception import ServiceException
from api.utils.validation import validate, safe_validate


class BaseRestServices:
    def process(self, data: Any) -> ServiceResponse[RESP]:
        start_time = timer()
        try:
            payload = data.get("payload")
            request = validate(self.request_model(), payload)
            data["payload"] = request
            request_params = validate(RequestParams, data)
            response, status = self.process_request(request_params, start_time)
            return self.process_response(request, response, status, start_time)
        except ValidationError as err:
            return self.handle_error(
                400, err.json(include_url=False, include_context=False), start_time
            )
        except pybit.exceptions.InvalidRequestError as err:
            return self.handle_error(err.status_code, err.message, start_time)
        except ServiceException as err:
            return self.handle_error(err.message, start_time)
        except Exception as err:
            return self.handle_error(503, f"Unexpected {err=}, {type(err)=}", start_time)

    def process_request(self, request_params: RequestParams, start_time: int) -> tuple[str, int]:
        log.debug(request_params)

        api_session = HTTP(
            demo=request_params.demo,
            testnet=request_params.testnet,
            api_key=request_params.api_key,
            api_secret=request_params.api_secret,
        )

        callee = getattr(api_session, self.SERVICE)
        response = callee(**request_params.payload.model_dump())

        return response, 200

    def process_response(
        self, request: REQ, response: Any, status: int, start_time: Decimal
    ) -> ServiceResponse[RESP]:
        return ServiceResponse(
            status=ServiceStatus.SUCCESS,
            data=self.transform_success_response(request, response),
            duration=round(timer() - start_time, 2),
        )

    def handle_error(
        self, status_code: int, message: str, start_time: Decimal
    ) -> ServiceResponse[RESP]:
        return ServiceResponse(
            status=ServiceStatus.ERROR,
            data=ErrorResponseData(status_code=status_code, result=message),
            duration=round(timer() - start_time, 2),
        )

    def transform_success_response(self, request: REQ, response: Any) -> RESP:
        model = self.response_model()
        return safe_validate(model, response)

    def transform_error_response(self, request: REQ, response: Any, status: int) -> str:
        return str(response)

    def request_model(self) -> Type[REQ]:
        raise NotImplementedError

    def response_model(self) -> Type[RESP]:
        raise NotImplementedError
