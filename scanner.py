import os
from tqdm import tqdm
from datetime import datetime
from string import ascii_uppercase
from analyser import Analyser
from exceptions import EmptyDirectoryException, InvalidDirectoryException

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
            return
    
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


class DiskUsage:
    def get_files_in_directory(self, directory) -> list[File]:
        """Возвращает список файлов в указанной директории."""
        if not os.path.exists(directory): 
            raise InvalidDirectoryException
        path = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                path.append(os.path.join(root, filename))
        return path

    def get_disk_usage(self, directory, extension_filter=None, date_filter=None) -> list[File]:
        """Вычисляет и выводит на экран использование дискового пространства с прогрессбаром."""
        if date_filter:
            date_filter = datetime.strptime(date_filter, "%d-%m-%Y")
        found = []
        paths = self.get_files_in_directory(directory)
        if not paths:
            raise EmptyDirectoryException
        for path in tqdm(paths, desc="Calculating Disk Usage", mininterval=0.01, unit='files'):
            file = File(path)
            if extension_filter and not Analyser.check_extension(file, extension_filter):
                continue
            if date_filter and not Analyser.check_creation_date(file, date_filter):
                continue
            found.append(file)
        
        return found