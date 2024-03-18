from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    GIGA_CREDENTIALS: str


async def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        GIGA_CREDENTIALS=env('AU_DATA')
    )

