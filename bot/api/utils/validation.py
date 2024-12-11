from typing import Any, Type

from pydantic import ValidationError

from utils.logger import log
from api.utils.const import MODEL


def validate(model: Type[MODEL], params: Any) -> MODEL:
    return model.model_validate(params)


def safe_validate(model: Type[MODEL], params: Any) -> MODEL:
    try:
        return validate(model, params)
    except ValidationError as err:
        log.warning(f"VALIDATION ERROR: {err.json(include_url=False, include_context=False)}")
        return model.model_construct(**params if params else {})
