from __future__ import annotations
import typing as ty

import os
import re
from dataclasses import dataclass


if not os.environ.get("ROOT_DIR"):
    os.environ["ROOT_DIR"] = os.path.dirname(__file__)


class ConfigSection:
    """
    Parent class for configuration sections.
    Provides set required fields and raises NotImplementedError if variable not set.
    Provides use string formatting in variables. Usage:
        ROOT_PATH=.
        STORAGE_PATH={os.environ[ROOT_PATH]}/storage
    Provides initialization from virtual environment in one line: `MySection.init()`
    """

    required_fields = []
    section_name = None

    def __init__(self, **kwargs): ...

    def __post_init__(self):
        for var_name in self.required_fields:  # Checking for required vars are set
            if self.__getattribute__(var_name) in {None, ""}:
                raise NotImplementedError(
                    f"{self.env_name(var_name)} not set in virtual environment"
                )
        self.format_values()

    def format_values(self) -> None:
        """
        Formatting variables.
        """
        for var_name, value in self.__dict__.items():
            if isinstance(value, str):
                self.__setattr__(var_name, (value := value.format(os=os)))
                os.environ[self.env_name(var_name)] = str(value)

    @classmethod
    def env_name(cls, var_name: str) -> str:
        """
        Creates full name of variable.
        >>> class MySection(ConfigSection):
        ...     variable: str = ""
        >>> MySection.env_name("variable")
        MY_SECTION_VARIABLE
        """
        section_name = (
            cls.section_name if cls.section_name is not None else cls.__name__
        )
        section_name = re.sub(r"\B([A-Z])", r"_\g<1>", section_name)
        return f"{f'{section_name.upper()}_' if section_name else ''}{var_name.upper()}"

    @classmethod
    def init(cls) -> ty.Self:
        """
        Initializes section based on environment variables.
        """
        kwargs = {}
        for param_name, param_type in ty.get_type_hints(cls).items():
            if issubclass(param_type, ConfigSection):  # recursive call
                kwargs[param_name] = param_type.init()
            else:
                value = os.getenv(cls.env_name(param_name)) or cls.__dict__.get(
                    param_name
                )
                if param_type is bool:
                    value = bool(int(value))
                kwargs[param_name] = value

        return cls(**kwargs)


@dataclass
class Base(ConfigSection):
    root_dir: str
    version: str

    required_fields = ["root_dir", "version"]
    section_name = ""

    def format_values(self) -> None:
        self.root_dir = os.path.abspath(self.root_dir)
        super(Base, self).format_values()


@dataclass
class Logging(ConfigSection):
    file: str
    level: str = "DEBUG"
    colorize: bool = False

    required_field = ["file"]


@dataclass
class TgBot(ConfigSection):
    enabled: bool
    token: str
    webhook: TgBotWebhook

    required_field = ["enabled", "token"]


@dataclass
class TgBotWebhook(ConfigSection):
    host: str
    enabled: bool = False
    secret_key: str = ""

    if int(os.environ.get("RUN_WEB_APP") or "0"):
        required_fields = ["host"]

    def __post_init__(self):
        if not self.secret_key:
            self.secret_key = os.getenv("TG_BOT_TOKEN")
        super(TgBotWebhook, self).__post_init__()


@dataclass
class WebApp(ConfigSection):
    enabled: bool

    required_fields = ["enabled"]


@dataclass
class Storage(ConfigSection):
    path: str

    required_fields = ["path"]


@dataclass
class Config(ConfigSection):
    base: Base
    logger: Logging
    tg_bot: TgBot
    web_app: WebApp
    storage: Storage


def load_config() -> Config:
    return Config.init()
