from __future__ import annotations

from typing import cast, List, Optional

import click
import pytest

from quart import (
    abort,
    Blueprint,
    Quart,
    render_template_string,
    request,
    ResponseReturnValue,
    websocket,
)
from quart.views import MethodView


@pytest.mark.asyncio
async def test_blueprint_route() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)

    @blueprint.route("/page/")
    async def route() -> ResponseReturnValue:
        return "OK"

    app.register_blueprint(blueprint)

    async with app.test_request_context("/page/"):
        assert request.blueprint == "blueprint"


@pytest.mark.asyncio
async def test_blueprint_websocket() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)

    @blueprint.websocket("/ws/")
    async def ws() -> None:
        while True:
            await websocket.send(websocket.blueprint.encode())

    app.register_blueprint(blueprint)

    test_client = app.test_client()
    async with test_client.websocket("/ws/") as test_websocket:
        result = await test_websocket.receive()
    assert cast(bytes, result) == b"blueprint"


@pytest.mark.asyncio
async def test_blueprint_url_prefix() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)
    prefix = Blueprint("prefix", __name__, url_prefix="/prefix")

    @app.route("/page/")
    @blueprint.route("/page/")
    @prefix.route("/page/")
    async def route() -> ResponseReturnValue:
        return "OK"

    app.register_blueprint(blueprint, url_prefix="/blueprint")
    app.register_blueprint(prefix)

    async with app.test_request_context("/page/"):
        assert request.blueprint is None

    async with app.test_request_context("/prefix/page/"):
        assert request.blueprint == "prefix"

    async with app.test_request_context("/blueprint/page/"):
        assert request.blueprint == "blueprint"


@pytest.mark.asyncio
async def test_blueprint_template_filter() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)

    @blueprint.app_template_filter()
    def reverse(value: str) -> str:
        return value[::-1]

    @blueprint.route("/")
    async def route() -> ResponseReturnValue:
        return await render_template_string("{{ name|reverse }}", name="hello")

    app.register_blueprint(blueprint)

    response = await app.test_client().get("/")
    assert b"olleh" in (await response.get_data())  # type: ignore


@pytest.mark.asyncio
async def test_blueprint_error_handler() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)

    @blueprint.route("/error/")
    async def error() -> ResponseReturnValue:
        abort(409)
        return "OK"

    @blueprint.errorhandler(409)
    async def handler(_: Exception) -> ResponseReturnValue:
        return "Something Unique", 409

    app.register_blueprint(blueprint)

    response = await app.test_client().get("/error/")
    assert response.status_code == 409
    assert b"Something Unique" in (await response.get_data())  # type: ignore


@pytest.mark.asyncio
async def test_blueprint_method_view() -> None:
    app = Quart(__name__)
    blueprint = Blueprint("blueprint", __name__)

    class Views(MethodView):
        async def get(self) -> ResponseReturnValue:
            return "GET"

        async def post(self) -> ResponseReturnValue:
            return "POST"

    blueprint.add_url_rule("/", view_func=Views.as_view("simple"))

    app.register_blueprint(blueprint)

    test_client = app.test_client()
    response = await test_client.get("/")
    assert "GET" == (await response.get_data(as_text=True))
    response = await test_client.post("/")
    assert "POST" == (await response.get_data(as_text=True))


@pytest.mark.parametrize(
    "cli_group, args",
    [
        ("named", ["named", "cmd"]),
        (None, ["cmd"]),
        (Ellipsis, ["blueprint", "cmd"]),
    ],
)
def test_cli_blueprints(cli_group: Optional[str], args: List[str]) -> None:
    app = Quart(__name__)

    blueprint = Blueprint("blueprint", __name__, cli_group=cli_group)

    @blueprint.cli.command("cmd")
    def command() -> None:
        click.echo("command")

    app.register_blueprint(blueprint)

    app_runner = app.test_cli_runner()
    result = app_runner.invoke(args=args)

    assert "command" in result.output


@pytest.mark.asyncio
async def test_nested_blueprint() -> None:
    app = Quart(__name__)

    parent = Blueprint("parent", __name__)
    child = Blueprint("child", __name__)
    grandchild = Blueprint("grandchild", __name__)

    @parent.errorhandler(403)
    async def forbidden(_: Exception) -> ResponseReturnValue:
        return "Parent no", 403

    @parent.route("/")
    async def parent_index() -> ResponseReturnValue:
        return "Parent yes"

    @parent.route("/no")
    async def parent_no() -> ResponseReturnValue:
        abort(403)

    @child.route("/")
    async def child_index() -> ResponseReturnValue:
        return "Child yes"

    @child.route("/no")
    async def child_no() -> ResponseReturnValue:
        abort(403)

    @grandchild.errorhandler(403)
    async def grandchild_forbidden(_: Exception) -> ResponseReturnValue:
        return "Grandchild no", 403

    @grandchild.route("/")
    async def grandchild_index() -> ResponseReturnValue:
        return "Grandchild yes"

    @grandchild.route("/no")
    async def grandchild_no() -> ResponseReturnValue:
        abort(403)

    child.register_blueprint(grandchild, url_prefix="/grandchild")
    parent.register_blueprint(child, url_prefix="/child")
    app.register_blueprint(parent, url_prefix="/parent")

    client = app.test_client()

    assert (await (await client.get("/parent/")).get_data()) == b"Parent yes"  # type: ignore
    assert (await (await client.get("/parent/child/")).get_data()) == b"Child yes"  # type: ignore
    assert (await (await client.get("/parent/child/grandchild/")).get_data()) == b"Grandchild yes"  # type: ignore  # noqa: E501
    assert (await (await client.get("/parent/no")).get_data()) == b"Parent no"  # type: ignore
    assert (await (await client.get("/parent/child/no")).get_data()) == b"Parent no"  # type: ignore
    assert (await (await client.get("/parent/child/grandchild/no")).get_data()) == b"Grandchild no"  # type: ignore  # noqa: E501
