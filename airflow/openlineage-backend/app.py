from typing import Any

from fastapi import FastAPI, Request, status


app = FastAPI(title="OpenLineage Event Receiver")
events: list[dict[str, Any]] = []
dbt_events: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/lineage", status_code=status.HTTP_201_CREATED)
async def receive_event(request: Request) -> dict[str, int]:
    event = await request.json()
    events.append(event)
    return {"stored": len(events)}


@app.post("/api/v1/dbt-lineage", status_code=status.HTTP_201_CREATED)
async def receive_dbt_event(request: Request) -> dict[str, int]:
    event = await request.json()
    dbt_events.append(event)
    return {"stored": len(dbt_events)}


@app.get("/events")
def list_events() -> dict[str, Any]:
    return {"count": len(events), "events": events}


@app.get("/dbt-events")
def list_dbt_events() -> dict[str, Any]:
    return {"count": len(dbt_events), "events": dbt_events}
