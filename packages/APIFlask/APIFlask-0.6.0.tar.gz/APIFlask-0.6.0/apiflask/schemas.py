from typing import Any
from typing import Dict

from marshmallow import Schema
from marshmallow.fields import Integer
from marshmallow.fields import URL


# schema for the detail object of validation error response
validation_error_detail_schema: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "<location>": {
            "type": "object",
            "properties": {
                "<field_name>": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
}


# schema for validation error response
validation_error_schema: Dict[str, Any] = {
    "properties": {
        "detail": validation_error_detail_schema,
        "message": {
            "type": "string"
        },
        "status_code": {
            "type": "integer"
        }
    },
    "type": "object"
}


# schema for generic error response
http_error_schema: Dict[str, Any] = {
    "properties": {
        "detail": {
            "type": "object"
        },
        "message": {
            "type": "string"
        },
        "status_code": {
            "type": "integer"
        }
    },
    "type": "object"
}


class EmptySchema(Schema):
    """An empty schema used to generate a 204 response.

    Example:

    ```python
    @app.delete('/foo')
    @output(EmptySchema)
    def delete_foo():
        return ''
    ```

    It equals to:

    ```python
    @app.delete('/foo')
    @output({}, 204)
    def delete_foo():
        return ''
    ```
    """

    pass


class PaginationSchema(Schema):
    page = Integer()
    per_page = Integer()
    pages = Integer()
    total = Integer()
    current = URL()
    next = URL()
    prev = URL()
    first = URL()
    last = URL()
