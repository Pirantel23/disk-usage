import os
from tqdm import tqdm
from datetime import datetime
from string import ascii_uppercase
from utils import Utils
from exceptions import EmptyDirectoryException, InvalidDirectoryException
from file import File

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
        for path in tqdm(paths, desc="Scanning files", mininterval=0.01, unit='files', miniters=1, smoothing=1):
            file = File(path)
            if extension_filter and not Utils.check_extension(file, extension_filter):
                continue
            if date_filter and not Utils.check_creation_date(file, date_filter):
                continue
            found.append(file)
        
        return found