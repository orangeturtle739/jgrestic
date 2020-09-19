from __future__ import annotations

import dataclasses
import json
import os
import typing as t


@dataclasses.dataclass
class Config:
    env: t.Dict[str, str]
    backup: Backup
    forget: Forget

    def extend_env(self) -> t.Dict[str, str]:
        return {**os.environ, **self.env}


@dataclasses.dataclass
class Backup:
    args: t.List[str]


@dataclasses.dataclass
class Forget:
    args: t.List[str]


T = t.TypeVar("T")


# https://gist.github.com/gatopeich/1efd3e1e4269e1e98fae9983bb914f22
def dataclass_from_dict(klass: t.Type[T], dikt: t.Any) -> T:
    try:
        hints = t.get_type_hints(klass)
        fieldtypes = {f.name: hints[f.name] for f in dataclasses.fields(klass)}
        bob = klass(**{f: dataclass_from_dict(fieldtypes[f], dikt[f]) for f in dikt})  # type: ignore
        return bob
    except Exception:
        return dikt


def load(data: t.TextIO) -> Config:
    return dataclass_from_dict(Config, json.load(data))
