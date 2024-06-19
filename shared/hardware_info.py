import datetime
from uuid import UUID

from pydantic import BaseModel


class Builder(BaseModel):
    builder_id: UUID
    distribution: str
    os_version: str
    hostname: str
    kernel_version: str
    architecture: str
    cpu_info: str
    pci_list: str
    startup_time: str
    ram_info: str
    last_ping: datetime.datetime | None = None
