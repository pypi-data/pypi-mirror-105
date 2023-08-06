import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import dotenv
import yaml
from pydantic import BaseModel
from pydantic.utils import deep_update

PREFIX = "reporting"


class TestRunSettings(BaseModel):
    display_name: str = "Default Suite"
    build: Optional[str] = None
    environment: Optional[str] = None
    context: Optional[str] = None


class ServerSettings(BaseModel):
    hostname: str
    access_token: str


class NotificationsSettings(BaseModel):
    slack_channels: Optional[str] = None
    ms_teams_channels: Optional[str] = None
    emails: Optional[str] = None


class MilestoneSettings(BaseModel):
    id: Optional[str]
    name: Optional[str]


class Settings(BaseModel):
    enabled: bool = True
    project_key: str = "DEF"
    send_logs: bool = True
    server: ServerSettings
    run: TestRunSettings = TestRunSettings()
    notifications: Optional[NotificationsSettings] = None
    milestone: Optional[MilestoneSettings] = None


def _list_settings(model: Type[BaseModel]) -> List:
    setting_names = []
    for field_name, field_value in model.__fields__.items():
        field_list = [field_name]
        if issubclass(field_value.type_, BaseModel):
            inner_fields = _list_settings(field_value.type_)
            inner_fields = [field_list + inner for inner in inner_fields]
            setting_names += inner_fields
        else:
            setting_names.append(field_list)

    return setting_names


def _put_by_path(settings_dict: dict, path: List[str], value: Any) -> None:
    if len(path) == 1:
        settings_dict[path[0]] = value
    else:
        current_dict = settings_dict.get(path[0], {})
        _put_by_path(current_dict, path[1:], value)
        settings_dict[path[0]] = current_dict


def _get_by_path(settings_dict: dict, path: List[str], default_value: Any = None) -> Any:
    if len(path) == 1:
        return settings_dict.get(path[0], default_value)
    else:
        inner_dict = settings_dict.get(path[0], {})
        return _get_by_path(inner_dict, path[1:], default_value)


def _load_env(path_list: List[List[str]]) -> dict:
    dotenv.load_dotenv(".env")
    settings: Dict[str, Any] = {}
    for path in path_list:
        env_name = "_".join([PREFIX] + path).upper()
        env_variable = os.getenv(env_name)
        if env_variable is not None:
            _put_by_path(settings, path, env_variable)

    return settings


def _load_yaml(path_list: List[List[str]]) -> Dict[str, Any]:
    settings: Dict[str, Any] = {}
    filename = Path("agent.yaml")
    if not filename.exists():
        filename = Path("agent.yml")
        if not filename.exists():
            return settings

    yaml_settings = yaml.safe_load(filename.read_text())
    for setting_path in path_list:
        yaml_path = [name.replace("_", "-") for name in [PREFIX] + setting_path]
        setting_value = _get_by_path(yaml_settings, yaml_path)
        if setting_value is not None:
            _put_by_path(settings, setting_path, setting_value)

    return settings


def load_settings() -> Settings:
    settings_path_list = _list_settings(Settings)
    settings: Dict[str, Any] = {}
    yaml_settings = _load_yaml(settings_path_list)
    settings = deep_update(settings, yaml_settings)
    env_settings = _load_env(settings_path_list)
    settings = deep_update(settings, env_settings)
    return Settings(**settings)
