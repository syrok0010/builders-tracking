import pathlib
from os.path import isfile
from subprocess import run

project_root_path = str(pathlib.Path().resolve())
crond_file_path = '/etc/cron.d/builder'


def cron_command(target_command: str):
    return f'* * * * * root {project_root_path}/.venv/bin/python {project_root_path}/main.py {target_command} \n'


def is_installed(result_command: str) -> bool:
    if not isfile(crond_file_path):
        return False
    with open(crond_file_path, 'r') as file:
        for line in file.readlines():
            if line == result_command:
                return True
    return False


def install(target_command: str, pre_install=None):
    if is_installed(cron_command(target_command)):
        raise Exception("Client or server is already installed on the machine")
    data = run('ps aux | grep -i crond', capture_output=True, shell=True, text=True)
    if len(data.stdout.splitlines()) <= 2:
        raise Exception('Crond should be installed correctly to run this application')
    if pre_install is not None:
        pre_install()
    with open(crond_file_path, 'a') as file:
        file.write(cron_command(target_command))
