import os
from datetime import datetime

class File:
    def __init__(self, path: str) -> None:
        self.path = path
        self.extension = self.get_extension()
        self.creation_date = self.get_creation_date()
        self.size = self.get_size()
    
    def __repr__(self) -> str:
        return f'{self.path}'

    def get_size(self) -> int:
        try:
            return os.path.getsize(self.path)
        except FileNotFoundError:
            return 0
    
    def get_extension(self) -> str:
        try:
            return os.path.splitext(self.path)[-1]
        except FileNotFoundError:
            return
    
    def get_creation_date(self) -> datetime:
        try:
            timestamp = os.path.getctime(self.path)
            return datetime.fromtimestamp(timestamp)
        except FileNotFoundError:
            return