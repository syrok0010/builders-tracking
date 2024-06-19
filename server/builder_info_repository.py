import datetime
import sqlite3
from os.path import isfile

from shared.hardware_info import Builder

db_name = 'builders.db'


class BuilderInfoRepository:
    def __init__(self):
        new_db = isfile(db_name)
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        if new_db:
            return

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Builders (
        id TEXT PRIMARY KEY,
        distribution TEXT NOT NULL,
        os_version TEXT NOT NULL,
        hostname TEXT NOT NULL,
        kernel_version TEXT NOT NULL,
        architecture TEXT NOT NULL,
        cpu_info TEXT NOT NULL,
        pci_list TEXT NOT NULL,
        startup_time TEXT NOT NULL,
        ram_info TEXT NOT NULL,
        last_ping TEXT NOT NULL,
        deactivated INT NOT NULL DEFAULT 0
        )
        ''')
        self.connection.commit()

    def add_builder(self, builder: Builder):
        print('New client connection established', builder.builder_id, builder.distribution)
        builder.last_ping = datetime.datetime.now(datetime.UTC)
        self.cursor.execute('''
        INSERT INTO Builders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        ''', tuple(map(str, builder.dict().values())))
        self.connection.commit()

    def update_last_ping(self, builder_id: str):
        sql = '''UPDATE Builders SET last_ping = datetime('now'), deactivated = 0 WHERE id ='''
        sql += f"'{builder_id.strip()}'"
        self.cursor.execute(sql)
        self.connection.commit()
        print(f'{builder_id} is still alive')

    def get_older_than_two_minutes(self) -> list[str]:
        self.cursor.execute('''
        SELECT id FROM Builders
        WHERE unixepoch('now') - unixepoch(Builders.last_ping) > 120 AND deactivated = 0
        ''')
        return self.cursor.fetchall()

    def mark_deactivated(self, ids: list[str]):
        ids_str = ', '.join(map(lambda x: f"'{x}'", ids))
        sql = f'UPDATE Builders SET deactivated = 1 WHERE id IN ({ids_str})'
        self.cursor.execute(sql)
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()