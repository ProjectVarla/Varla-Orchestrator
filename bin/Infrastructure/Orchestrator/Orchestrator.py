from dataclasses import dataclass
from typing import Optional

import yaml
from conf import settings
from dotenv import load_dotenv
from fastapi import Response
from fastapi import status as status_code
from yaml.loader import SafeLoader

from .Service import Service

load_dotenv()


@dataclass
class Orchestrator:
    services: dict[str, Service]

    def __init__(self) -> None:
        Orchestrator.services = {}
        self.load_configurations()

    def __getitem__(self, __name: str) -> Service:
        return self.services[__name]

    def __iter__(self):
        for key in self.services:
            yield self.services[key]

    def add(self, service: Service):
        self.services[service.tmux_name] = service
        return self

    def get_service_status(
        self, service_name: str, response: Optional[Response] = None
    ):
        try:
            return (
                f"{service_name} is up!"
                if self[service_name].is_up
                else f"{service_name} is down!"
            )
        except KeyError:
            if response:
                response.status_code = status_code.HTTP_404_NOT_FOUND
            return f"`{service_name}` service was not found!"

    def start_service(self, service_name: str, response: Optional[Response] = None):
        try:
            if self[service_name].is_up:
                if response:
                    response.status_code = status_code.HTTP_208_ALREADY_REPORTED
                return f"{service_name} is already up!"
            else:
                self[service_name].up()
                if response:
                    response.status_code = status_code.HTTP_200_OK
                return f"{service_name} is up!"
        except KeyError:
            if response:
                response.status_code = status_code.HTTP_404_NOT_FOUND
            return f"`{service_name}` service Service was not found!"

    def stop_service(self, service_name: str, response: Optional[Response] = None):
        try:
            if not self[service_name].is_up:
                if response:
                    response.status_code = status_code.HTTP_208_ALREADY_REPORTED
                return f"{service_name} is already down!"
            else:
                self[service_name].down()
                if response:
                    response.status_code = status_code.HTTP_200_OK
                return f"{service_name} is down!"

        except KeyError:
            if response:
                response.status_code = status_code.HTTP_404_NOT_FOUND
            return f"`{service_name}` service was not found!"

    def restart_service(self, service_name: str, response: Optional[Response] = None):
        try:
            if not self[service_name].is_up:
                if response:
                    response.status_code = status_code.HTTP_200_OK
                self[service_name].up()
                return f"{service_name} is already down, Starting Service!"
            else:
                self[service_name].restart()
                if response:
                    response.status_code = status_code.HTTP_200_OK
                return f"{service_name} was restarted!"

        except KeyError:
            if response:
                response.status_code = status_code.HTTP_404_NOT_FOUND
            return f"`{service_name}` service was not found!"

    def load_configurations(self):
        with open(settings.SERVICES_CONFIG_PATH, "r") as f:
            configs = yaml.load(f, Loader=SafeLoader)
            for config in configs["services"]:
                self.services[config["tmux_name"]] = Service(**config)
