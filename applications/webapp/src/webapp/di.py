from pathlib import Path

from core.settings import Settings as CoreSettings
from fastapi.templating import Jinja2Templates
from that_depends import BaseContainer
from that_depends.providers import (
    Factory,
    Singleton,
)

from webapp.settings import Settings


def create_templates(
    template_dir: Path, core_settings: CoreSettings
) -> Jinja2Templates:
    templates = Jinja2Templates(directory=template_dir)
    templates.env.globals["version"] = core_settings.version
    templates.env.globals["dev"] = core_settings.DEV
    templates.env.globals["repo_url"] = "https://github.com/oliverlambson/bootstr.app"
    return templates


class Deps(BaseContainer):
    app_root: Singleton[Path] = Singleton(lambda: Path(__file__).parent)
    template_dir: Singleton[Path] = Singleton(
        lambda: Path(__file__).parent / "templates"
    )
    static_dir: Singleton[Path] = Singleton(lambda: Path(__file__).parent / "static")

    settings: Singleton[Settings] = Singleton(Settings)  # pyright: ignore[reportCallIssue]
    core_settings: Singleton[CoreSettings] = Singleton(CoreSettings)  # pyright: ignore[reportCallIssue]

    templates: Factory[Jinja2Templates] = Factory(
        create_templates,
        template_dir=template_dir.cast,
        core_settings=core_settings.cast,
    )
