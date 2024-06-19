from server.builder_info_repository import BuilderInfoRepository
from time import sleep


def mark_deactivated():
    sleep(1)
    repo = BuilderInfoRepository()
    ids = repo.get_older_than_two_minutes()
    ids = [x[0] for x in ids]
    for builder_id in ids:
        print(f'Client {builder_id} is down')
    repo.mark_deactivated(ids)
