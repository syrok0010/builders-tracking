import os
import pathlib
import platform
from subprocess import run
from uuid import uuid4

import requests

from shared.hardware_info import Builder

project_root_path = str(pathlib.Path().resolve())


def initial_send_hwinfo():
    builder_id = uuid4()
    info = platform.freedesktop_os_release()
    uname = os.uname()
    cpu_info = run('lscpu', capture_output=True, shell=True, text=True).stdout
    pci_list = run('lspci', capture_output=True, shell=True, text=True).stdout
    ram_info = run('dmidecode -t 17', capture_output=True, shell=True, text=True).stdout
    startup_time = run('date -d "`cut -f1 -d. /proc/uptime` seconds ago"', capture_output=True, shell=True, text=True).stdout
    hw_info = Builder(
        builder_id=builder_id,
        distribution=info['PRETTY_NAME'],
        os_version=info['BUILD_ID'],
        hostname=uname.nodename,
        kernel_version=uname.release,
        architecture=uname.machine,
        cpu_info=cpu_info,
        pci_list=pci_list,
        startup_time=startup_time,
        ram_info=ram_info
    )
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    content: str = hw_info.model_dump_json()
    data = requests.post('http://localhost:8000/init', data=content, headers=headers)
    if data.status_code != 200:
        raise Exception('Installation failed')
    with open('/etc/builder-uuid', 'w') as f:
        f.write(str(builder_id))


def ping():
    with open('/etc/builder-uuid', 'r') as f:
        builder_id = f.readline()
        requests.post('http://localhost:8000/ping/' + builder_id)
