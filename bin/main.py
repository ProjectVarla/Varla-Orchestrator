import uvicorn
from fastapi import FastAPI, Response, status as status_code
from Infrastructure import Orchestrator
from VarlaLib.Shell import varla_header
from conf import settings

app = FastAPI(title="Varla-Orchestrator")
orchestrator = Orchestrator()


@app.get("/up/{service_name}")
def up(service_name: str, response: Response) -> str:
    try:
        if orchestrator[service_name].is_up:
            response.status_code = status_code.HTTP_208_ALREADY_REPORTED
            return "Service is already up!"
        else:
            orchestrator[service_name].up()
            response.status_code = status_code.HTTP_200_OK
            return "Service is up!"

    except KeyError:
        response.status_code = status_code.HTTP_404_NOT_FOUND
        return "Service was not found!"


@app.get("/status/{service_name}")
def status(service_name: str, response: Response) -> bool:
    try:
        return (
            f"{service_name} is up!"
            if orchestrator[service_name].is_up
            else f"{service_name} is down!"
        )
    except KeyError:
        response.status_code = status_code.HTTP_404_NOT_FOUND
        return "Service was not found!"


@app.get("/down/{service_name}")
def down(service_name: str, response: Response) -> str:
    try:
        if not orchestrator[service_name].is_up:
            response.status_code = status_code.HTTP_208_ALREADY_REPORTED
            return "Service is already down!"
        else:
            orchestrator[service_name].down()
            response.status_code = status_code.HTTP_200_OK
            return "Service is down!"

    except KeyError:
        response.status_code = status_code.HTTP_404_NOT_FOUND
        return "Service was not found!"


@app.get("/restart/{service_name}")
def restart(service_name: str, response: Response) -> str:
    try:
        if not orchestrator[service_name].is_up:
            response.status_code = status_code.HTTP_200_OK
            orchestrator[service_name].up()
            return "Service is already down, Starting Service!"
        else:
            orchestrator[service_name].restart()
            response.status_code = status_code.HTTP_200_OK
            return "Service was restarted!"

    except KeyError:
        response.status_code = status_code.HTTP_404_NOT_FOUND
        return "Service was not found!"


if __name__ == "__main__":
    varla_header()
    uvicorn.run(
        "main:app",
        host=settings.ORCHESTRATOR_HOST,
        port=settings.ORCHESTRATOR_PORT,
    )
