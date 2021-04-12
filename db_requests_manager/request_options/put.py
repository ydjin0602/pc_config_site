import typing as t
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class OSConfig:
    name: t.Optional[t.Text] = None
    version: t.Optional[t.Text] = None


@dataclass_json
@dataclass(frozen=True)
class ProcessorConfig:
    name: t.Optional[t.Text] = None
    architecture: t.Optional[t.Text] = None
    temperature: t.Optional[t.Text] = None
    loading: t.Optional[t.Text] = None


@dataclass_json
@dataclass(frozen=True)
class SocketInfoConfig:
    host: t.Optional[t.Text] = None
    ip_address: t.Optional[t.Text] = None
    mac_address: t.Optional[t.Text] = None


@dataclass_json
@dataclass(frozen=True)
class DiskConfig:
    memory: t.Optional[t.Text] = None
    loading: t.Optional[t.Text] = None


@dataclass_json
@dataclass(frozen=True)
class PutConfigOptions:
    token: t.Text
    os: t.Optional[OSConfig] = None
    processor: t.Optional[ProcessorConfig] = None
    socket_info: t.Optional[SocketInfoConfig] = None
    disk: t.Optional[DiskConfig] = None
    ram: t.Optional[t.Text] = None