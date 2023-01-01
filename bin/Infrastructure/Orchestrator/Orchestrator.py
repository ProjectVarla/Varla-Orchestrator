from dataclasses import dataclass

import yaml
from conf import settings
from dotenv import load_dotenv
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

    def load_configurations(self):
        with open(settings.SERVICES_CONFIG_PATH, "r") as f:
            configs = yaml.load(f, Loader=SafeLoader)
            for config in configs["services"]:
                self.services[config["tmux_name"]] = Service(**config)
