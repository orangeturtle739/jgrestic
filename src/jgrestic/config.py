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
    secret_env_files: t.List[str] = dataclasses.field(default_factory=list)

    def read_secret_env_files(self) -> t.Dict[str, str]:
        result = {}
        for secret_env_file in self.secret_env_files:
            with open(secret_env_file, "r") as f:
                result.update(json.load(f))
        return result

    def extend_env(self) -> t.Dict[str, str]:
        return {**os.environ, **self.env, **self.read_secret_env_files()}


@dataclasses.dataclass
class Backup:
    args: t.List[str]


@dataclasses.dataclass
class Forget:
    args: t.List[str]


if t.TYPE_CHECKING:
    from _typeshed import DataclassInstance

    T = t.TypeVar("T", bound=DataclassInstance)
else:
    T = t.TypeVar(
        "T",
    )


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
