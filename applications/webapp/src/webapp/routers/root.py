from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from webapp.di import Deps

router = APIRouter()


@router.get("/", name="home")
async def home(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(Deps.templates)],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.jinja",
        {},
    )


@router.get("/about", name="about")
async def about(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(Deps.templates)],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "about.jinja",
        {},
    )


class Healthz(BaseModel):
    status: Literal["OK"]


@router.get("/healthz")
async def healthz() -> Healthz:
    return Healthz(status="OK")
