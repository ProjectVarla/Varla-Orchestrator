import uvicorn
from conf import settings
from fastapi import FastAPI, Response
from Infrastructure import Orchestrator
from Models import ServicesFilter
from VarlaLib.Shell import varla_header

app = FastAPI(title="Varla-Orchestrator")
orchestrator = Orchestrator()


@app.post("/status/{service_name}")
def status(service_name: str, response: Response) -> bool:
    return orchestrator.get_service_status(service_name, response)


@app.post("/status")
def status_list(services_filter: ServicesFilter) -> bool:
    print(services_filter)
    if services_filter.select_all:
        return [
            orchestrator.get_service_status(service.tmux_name)
            for service in orchestrator
        ]
    else:
        return [
            orchestrator.get_service_status(service_name)
            for service_name in services_filter
        ]


@app.post("/up/{service_name}")
def up(service_name: str, response: Response) -> str:
    return orchestrator.start_service(service_name, response)


@app.post("/up")
def up_list(services_filter: ServicesFilter) -> bool:
    if services_filter.select_all:
        return [
            orchestrator.start_service(service.tmux_name) for service in orchestrator
        ]
    else:
        return [
            orchestrator.start_service(service_name) for service_name in services_filter
        ]


@app.post("/down/{service_name}")
def down(service_name: str, response: Response) -> str:
    return orchestrator.stop_service(service_name, response)


@app.post("/down")
def down_list(services_filter: ServicesFilter) -> bool:
    return [orchestrator.stop_service(service_name) for service_name in services_filter]


@app.post("/restart/{service_name}")
def restart(service_name: str, response: Response) -> str:
    return orchestrator.restart_service(service_name, response)


@app.post("/restart")
def restart_list(services_filter: ServicesFilter) -> bool:
    return [
        orchestrator.restart_service(service_name) for service_name in services_filter
    ]


@app.post("/list")
def list() -> str:
    return [service.tmux_name for service in orchestrator]


if __name__ == "__main__":
    varla_header()
    uvicorn.run(
        "main:app",
        host=settings.ORCHESTRATOR_HOST,
        port=settings.ORCHESTRATOR_PORT,
    )
