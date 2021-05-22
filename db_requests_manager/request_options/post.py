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
    total_cores: int
    max_frequency: t.Text
    current_frequency: t.Text
    temperature: t.Text
    loading: t.Text
    usage_per_core: t.Text


@dataclass_json
@dataclass(frozen=True)
class SocketInfoConfig:
    host: t.Text
    ip_address: t.Text
    mac_address: t.Text


@dataclass_json
@dataclass(frozen=True)
class DiskConfig:
    file_system_type: t.Text
    total_memory: t.Text
    available: t.Text
    used: t.Text
    used_in_percents: t.Text


@dataclass_json
@dataclass
class RAMConfig:
    total_memory: t.Text
    available: t.Text
    used: t.Text
    used_in_percents: t.Text


@dataclass_json
@dataclass(frozen=True)
class PostConfigOptions:
    token: t.Text
    os: OSConfig
    processor: ProcessorConfig
    socket_info: SocketInfoConfig
    disk: DiskConfig
    ram: RAMConfig
