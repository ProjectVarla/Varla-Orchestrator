from os import system
from time import sleep
from typing import Optional

from libtmux import Pane
from libtmux import Server as Tmux
from libtmux import Session, Window
from libtmux.exc import TmuxSessionExists
from pydantic import BaseModel

tmux = Tmux()


class Service(BaseModel):
    tmux_session: str
    runtime_environment: str
    service_executable: str
    service_directory: str
    tmux_name: str
    auto_run: bool = False

    def __init__(self, **data) -> None:
        super().__init__(**data)

        if self.auto_run and not self.is_up:
            self.up()

    @property
    def session(self) -> Session:
        try:
            return tmux.new_session(
                session_name=self.tmux_session, window_name=self.tmux_name
            )
        except TmuxSessionExists:
            return tmux.find_where({"session_name": self.tmux_session})

    @property
    def window(self) -> Window:
        return self.session.attached_window

    @property
    def pane(self) -> Pane:
        return self.session.attached_pane

    @property
    def run_command(self) -> str:
        return f"{self.runtime_environment} {self.service_executable}"

    @property
    def is_up(self) -> bool:
        return not system(f'ps -x | grep "{self.run_command}" | grep -q -v "grep"')

    def up(self) -> None:
        self.pane.send_keys(f"cd {self.service_directory}")
        self.pane.send_keys(self.run_command)

    def down(self) -> None:
        self.pane.send_keys("^c")

    def restart(self) -> None:
        self.down()
        sleep(5)
        self.up()

    def kill(self):
        self.session.kill_session()
