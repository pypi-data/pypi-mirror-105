from collections.abc import Mapping as ABCMapping
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type
from typing import Union

from flask import current_app
from flask import jsonify
from flask import Response
from marshmallow import ValidationError as MarshmallowValidationError
from webargs.flaskparser import FlaskParser as BaseFlaskParser

from .exceptions import _ValidationError
from .schemas import EmptySchema
from .schemas import Schema
from .types import DecoratedType
from .types import HTTPAuthType
from .types import RequestType
from .types import ResponseType
from .types import SchemaType
from .helpers import _sentinel


class FlaskParser(BaseFlaskParser):
    """Overwrite the default `webargs.FlaskParser.handle_error`.

    Update the default status code and the error description from related
    configuration variables.
    """

    def handle_error(  # type: ignore
        self,
        error: MarshmallowValidationError,
        req: RequestType,
        schema: Schema,
        *,
        error_status_code: int,
        error_headers: Mapping[str, str]
    ) -> None:
        raise _ValidationError(
            error_status_code or current_app.config['VALIDATION_ERROR_STATUS_CODE'],
            current_app.config['VALIDATION_ERROR_DESCRIPTION'],
            error.messages,
            error_headers
        )


parser: FlaskParser = FlaskParser()
use_args: Callable = parser.use_args


def _annotate(f: Any, **kwargs: Any) -> None:
    if not hasattr(f, '_spec'):
        f._spec = {}
    for key, value in kwargs.items():
        f._spec[key] = value


def auth_required(
    auth: HTTPAuthType,
    role: Optional[str] = None,
    roles: Optional[list] = None,
    optional: Optional[str] = None
) -> Callable[[DecoratedType], DecoratedType]:
    """Protect a view with provided authentication settings.

    > Be sure to put it under the routes decorators (i.e., `app.route`, `app.get`,
    `app.post`, etc.).

    Examples:

    ```python
    from apiflask import APIFlask, HTTPTokenAuth, auth_required

    app = APIFlask(__name__)
    auth = HTTPTokenAuth()

    @app.get('/')
    @auth_required(auth)
    def hello():
        return 'Hello'!
    ```

    Arguments:
        auth: The `auth` object, an instance of [`HTTPBasicAuth`][apiflask.security.HTTPBasicAuth]
            or [`HTTPTokenAuth`][apiflask.security.HTTPTokenAuth].
        role: The selected role to allow to visit this view, accepts a string.
            See [Flask-HTTPAuth's documentation][_role]{target:_blank} for more details.
            [_role]: https://flask-httpauth.readthedocs.io/en/latest/#user-roles
        roles: Similar to `role` but accepts a list of role names.
        optional: Set to `True` to allow the view to execute even the authentication
            information is not included with the request, in which case the attribute
            `auth.current_user` will be `None`.

    *Version changed: 0.4.0*

    - Add parameter `roles`.
    """
    _roles = None
    if role is not None:
        _roles = [role]
    elif roles is not None:
        _roles = roles

    def decorator(f):
        _annotate(f, auth=auth, roles=_roles or [])
        return auth.login_required(role=_roles, optional=optional)(f)
    return decorator


def _generate_schema_from_mapping(
    schema: dict,
    schema_name: Optional[str]
) -> Type[Schema]:
    if schema_name is None:
        schema_name = 'GeneratedSchema'
    return Schema.from_dict(schema, name=schema_name)()


def input(
    schema: SchemaType,
    location: str = 'json',
    schema_name: Optional[str] = None,
    example: Optional[Any] = None,
    examples: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> Callable[[DecoratedType], DecoratedType]:
    """Add input settings for view functions.

    > Be sure to put it under the routes decorators (i.e., `app.route`, `app.get`,
    `app.post`, etc.).

    If the validation passed, the data will inject into view
    function as a positional argument in the form of `dict`. Otherwise,
    an error response with the detail of the validation result will be returned.

    Examples:

    ```python
    from apiflask import APIFlask, input

    app = APIFlask(__name__)

    @app.get('/')
    @input(PetInSchema)
    def hello(parsed_and_validated_input_data):
        print(parsed_and_validated_input_data)
        return 'Hello'!
    ```

    Arguments:
        schema: The Marshmallow schema of the input data.
        location: The location of the input data, one of `'json'` (default),
            `'files'`, `'form'`, `'cookies'`, `'headers'`, `'query'`
            (same as `'querystring'`).
        schema_name: The schema name for dict schema, only needed when you pass
            a `dict` schema (e.g., `{'name': String(required=True)}`) for `json`
            location.
        example: The example data in dict for request body, you should use either
            `example` or `examples`, not both.
        examples: Multiple examples for request body, you should pass a dict
            that contains multiple examples. Example:

            ```python
            {
                'example foo': {  # example name
                    'summary': 'an example of foo',  # summary field is optional
                    'value': {'name': 'foo', 'id': 1}  # example value
                },
                'example bar': {
                    'summary': 'an example of bar',
                    'value': {'name': 'bar', 'id': 2}
                },
            }
            ```

    *Version changed: 0.4.0*

    - Add parameter `examples`.
    """
    if isinstance(schema, ABCMapping):
        schema = _generate_schema_from_mapping(schema, schema_name)
    if isinstance(schema, type):  # pragma: no cover
        schema = schema()  # type: ignore

    def decorator(f):
        if location not in [
            'json', 'query', 'headers', 'cookies', 'files', 'form', 'querystring'
        ]:
            raise RuntimeError(
                'Unknown input location. The supported locations are: "json", "files",'
                ' "form", "cookies", "headers", "query" (same as "querystring").'
                f' Got "{location}" instead.'
            )
        if location == 'json':
            _annotate(f, body=schema, body_example=example, body_examples=examples)
        else:
            if not hasattr(f, '_spec') or f._spec.get('args') is None:
                _annotate(f, args=[])
            # Todo: Support set example for request parameters
            f._spec['args'].append((schema, location))
        return use_args(schema, location=location, **kwargs)(f)
    return decorator


def output(
    schema: SchemaType,
    status_code: int = 200,
    description: Optional[str] = None,
    schema_name: Optional[str] = None,
    example: Optional[Any] = None,
    examples: Optional[Dict[str, Any]] = None
) -> Callable[[DecoratedType], DecoratedType]:
    """Add output settings for view functions.

    > Be sure to put it under the routes decorators (i.e., `app.route`, `app.get`,
    `app.post`, etc.).

    The decorator will format the return value of your view function with
    provided Marshmallow schema. You can return a dict or an object (such
    as a model class instance of ORMs). APIFlask will handle the formatting
    and turn your return value into a JSON response.

    P.S. The output data will not be validated; it's a design choice of Marshmallow.
    Marshmallow 4.0 may be support the output validation.

    Examples:

    ```python
    from apiflask import APIFlask, output

    app = APIFlask(__name__)

    @app.get('/')
    @output(PetOutSchema)
    def hello():
        return the_dict_or_object_match_petout_schema
    ```

    Arguments:
        schema: The schemas of the output data.
        status_code: The status code of the response, defaults to `200`.
        description: The description of the response.
        schema_name: The schema name for dict schema, only needed when you pass
            a `dict` schema (e.g., `{'name': String()}`).
        example: The example data in dict for response body, you should use either
            `example` or `examples`, not both.
        examples: Multiple examples for response body, you should pass a dict
            that contains multiple examples. Example:

            ```python
            {
                'example foo': {  # example name
                    'summary': 'an example of foo',  # summary field is optional
                    'value': {'name': 'foo', 'id': 1}  # example value
                },
                'example bar': {
                    'summary': 'an example of bar',
                    'value': {'name': 'bar', 'id': 2}
                },
            }
            ```
    *Version changed: 0.6.0*

    - Support decorating async views.

    *Version changed: 0.5.2*

    - Return the `Response` object directly.

    *Version changed: 0.4.0*

    - Add parameter `examples`.
    """
    if schema == {}:
        schema = EmptySchema
    if isinstance(schema, ABCMapping):
        schema = _generate_schema_from_mapping(schema, schema_name)
    if isinstance(schema, type):  # pragma: no cover
        schema = schema()  # type: ignore

    if isinstance(schema, EmptySchema):
        status_code = 204

    def decorator(f):
        _annotate(f, response={
            'schema': schema,
            'status_code': status_code,
            'description': description,
            'example': example,
            'examples': examples
        })

        def _jsonify(obj, many=_sentinel, *args, **kwargs):  # pragma: no cover
            """From Flask-Marshmallow, see the NOTICE file for license informaiton."""
            if many is _sentinel:
                many = schema.many
            data = schema.dump(obj, many=many)  # type: ignore
            return jsonify(data, *args, **kwargs)

        @wraps(f)
        def _response(*args: Any, **kwargs: Any) -> ResponseType:
            if hasattr(current_app, 'ensure_sync'):  # pragma: no cover
                rv = current_app.ensure_sync(f)(*args, **kwargs)
            else:
                rv = f(*args, **kwargs)  # for Flask < 2.0
            if isinstance(rv, Response):
                return rv
            if not isinstance(rv, tuple):
                return _jsonify(rv), status_code
            json = _jsonify(rv[0])
            if len(rv) == 2:
                rv = (json, rv[1]) if isinstance(rv[1], int) else (json, status_code, rv[1])
            elif len(rv) >= 3:
                rv = (json, rv[1], rv[2])
            else:
                rv = (json, status_code)
            return rv
        return _response
    return decorator


def doc(
    summary: Optional[str] = None,
    description: Optional[str] = None,
    tag: Optional[str] = None,
    tags: Optional[List[str]] = None,
    responses: Optional[Union[List[int], Dict[int, str]]] = None,
    deprecated: Optional[bool] = None,
    hide: Optional[bool] = None
) -> Callable[[DecoratedType], DecoratedType]:
    """Set up the OpenAPI Spec for view functions.

    > Be sure to put it under the routes decorators (i.e., `app.route`, `app.get`,
    `app.post`, etc.).

    Examples:

    ```python
    from apiflask import APIFlask, doc

    app = APIFlask(__name__)

    @app.get('/')
    @doc(summary='Say hello', tag='Foo')
    def hello():
        return 'Hello'
    ```

    Arguments:
        summary: The summary of this endpoint. If not set, the name of the view function
            will be used. If your view function is named with `get_pet`, then the summary
            will be "Get Pet". If the view function has a docstring, then the first
            line of the docstring will be used. The precedence will be:

            ```
            @doc(summary='blah') > the first line of docstring > the view function name
            ```

        description: The description of this endpoint. If not set, the lines after the empty
            line of the docstring will be used.
        tag: The tag name of this endpoint, map the tags you passed in the `app.tags`
            attribute. If `app.tags` is not set, the blueprint name will be used as
            tag name.
        tags: Similar to `tag` but accepts a list of tag names.
        responses: The other responses for this view function, accepts a dict in a format
            of `{404: 'Not Found'}` or a list of status code (`[404, 418]`).
        deprecated: Flag this endpoint as deprecated in API docs. Defaults to `False`.
        hide: Hide this endpoint in API docs. Defaults to `False`.

    *Version changed: 0.5.0*

    - Change the default value of parameters `hide` and `deprecated` from `False` to `None`.

    *Version changed: 0.4.0*

    - Add parameter `tag`.

    *Version changed: 0.3.0*

    - Change the default value of `deprecated` from `None` to `False`.
    - Rename parameter `tags` to `tag`.

    *Version added: 0.2.0*
    """
    _tags = None
    if tag is not None:
        _tags = [tag]
    elif tags is not None:
        _tags = tags

    def decorator(f):
        _annotate(
            f,
            summary=summary,
            description=description,
            tags=_tags,
            responses=responses,
            deprecated=deprecated,
            hide=hide
        )
        return f
    return decorator
