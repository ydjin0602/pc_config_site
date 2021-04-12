import typing as t
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class OSConfig:
    name: t.Text
    version: t.Text


@dataclass_json
@dataclass(frozen=True)
class ProcessorConfig:
    name: t.Text
    architecture: t.Text
    temperature: t.Text
    loading: t.Text


@dataclass_json
@dataclass(frozen=True)
class SocketInfoConfig:
    host: t.Text
    ip_address: t.Text
    mac_address: t.Text


@dataclass_json
@dataclass(frozen=True)
class DiskConfig:
    memory: t.Text
    loading: t.Text


@dataclass_json
@dataclass(frozen=True)
class PostConfigOptions:
    token: t.Text
    os: OSConfig
    processor: ProcessorConfig
    socket_info: SocketInfoConfig
    disk: DiskConfig
    ram: t.Text
