import hashlib
import os
import shutil
from pathlib import Path
from typing import Optional, List

from src import config
from src import db
from src import exceptions


class Storage:

    @classmethod
    def save(cls, user: str, data: bytes) -> str:
        md5 = hashlib.md5(data).hexdigest()
        file_path = cls.get_file_path(md5)
        db.save_to_db(user=user, file_hash=md5, file_path=file_path)
        cls._save_to_file(file_hash=md5, file_path=file_path, data=data)
        return md5

    @classmethod
    def read(cls, file_hash: str) -> Optional[bytes]:
        file_path = cls.get_file_path(file_hash)
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            raise exceptions.FileNotFound

    @classmethod
    def delete(cls, user: str, file_hash: str):
        file_dir = cls.get_file_dir(file_hash)
        db.remove_from_db(user=user, file_hash=file_hash)
        try:
            shutil.rmtree(file_dir)
        except FileNotFoundError:
            raise exceptions.FileNotFound
        return

    @classmethod
    def get_names(cls) -> List[str]:
        result = []
        for _, _, files in os.walk(config.STORAGE_PATH):
            result.extend(files)
        return result

    @classmethod
    def _save_to_file(cls, file_hash: str, file_path: str, data: bytes):
        file_dir = cls.get_file_dir(file_hash)
        Path(file_dir).mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(data)

    @classmethod
    def get_file_path(cls, file_hash: str) -> str:
        file_dir = cls.get_file_dir(file_hash)
        return f'{file_dir}/{file_hash}'

    @classmethod
    def get_file_dir(cls, file_hash: str) -> str:
        return f'{config.STORAGE_PATH}/{file_hash[:2]}'
