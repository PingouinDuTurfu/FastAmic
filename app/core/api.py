import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.core.service_dependency_injector_container import ServiceDIContainer

def load_json(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open(encoding='utf-8') as f:
        return json.load(f)


def init_di_container(api_directory: str) -> ServiceDIContainer:
    container = ServiceDIContainer()

    config_json = load_json(api_directory + "/config.json")
    container.config.from_dict(config_json)

    module_base = api_directory.replace('/', '.')
    modules = [module_base + '.' + module for module in config_json.get('injected_routes', [])]

    container.wire(modules=modules)

    return container

def lifespan_factory(api_directory: str):

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.container = init_di_container(api_directory)

        await app.container.mysql_service().connect()
        await app.container.rmq_service().connect()
        await app.container.log_service().start()
        yield
        await app.container.shutdown_services()

    return lifespan


