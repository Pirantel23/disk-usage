import os
from tqdm import tqdm
from datetime import datetime
from string import ascii_uppercase
from utils import Utils
from exceptions import EmptyDirectoryException, InvalidDirectoryException, InvalidSizeFormat
from file import File
import coloring as cl


EXCLUDED_EXTENSIONS = ['.tmp', '.bak', '.log']

class DiskUsage:
    def __init__(self, directory, extension_filter: str = None, date_filter: str = None, size_filter: str = None, author_filter: str = None, nested_filter: str = None):
        self.directory = directory
        self.extension_filter = extension_filter
        self.date_filter = datetime.strptime(date_filter, "%d-%m-%Y") if date_filter else None
        if size_filter:
            try:
                splitted_size = size_filter.split('-')
                self.min_size = Utils.downscale_units(splitted_size[0])
                self.max_size = Utils.downscale_units(splitted_size[1])
            except InvalidSizeFormat:
                print(f'{cl.RED}Size format is invalid.')
                self.min_size, self.max_size = None, None
        else:
            self.min_size, self.max_size = None, None
        
        if nested_filter:
            splitted_nested = nested_filter.split('-')
            self.min_nested = int(splitted_nested[0])
            self.max_nested = int(splitted_nested[1])
        else:
            self.min_nested, self.max_nested = None, None

        self.author_filter = author_filter

        self.print_filters()

    def print_filters(self) -> None:
        if self.extension_filter:
            print(f'{cl.YELLOW}Extension filter set to {self.extension_filter}{cl.RESET}')
        if self.date_filter:
            print(f'{cl.YELLOW}Date filter set to {self.date_filter}{cl.RESET}')
        if isinstance(self.min_size, int) and isinstance(self.max_size, int):
            print(f'{cl.YELLOW}Size filter set from {self.min_size}b to {self.max_size}b{cl.RESET}')
        if self.min_nested and self.max_nested:
            print(f'{cl.YELLOW}Nested level filter set from {self.min_nested} to {self.max_nested}{cl.RESET}')

    def get_files_in_directory(self) -> list[File]:
        if not os.path.exists(self.directory): 
            raise InvalidDirectoryException
        paths = []
        for root, _, filenames in tqdm(os.walk(self.directory), desc=f'{cl.YELLOW}Looking for directories in {self.directory}{cl.RESET}  ', unit = 'dirs'):
            for filename in filenames:
                paths.append(os.path.join(root, filename))
        return paths

    def apply_filters(self, file: File) -> bool:
        if self.extension_filter and not Utils.check_extension(file, self.extension_filter):
            return False
        if self.date_filter and not Utils.check_creation_date(file, self.date_filter):
            return False
        if isinstance(self.min_size, int) and isinstance(self.max_size, int) and not Utils.check_size(file, self.min_size, self.max_size):
            return False
        if self.min_nested and self.max_nested and not Utils.check_nested_level(file, self.min_nested, self.max_nested):
            return False
        return True

    def get_disk_usage(self) -> list[File]:
        found = []
        paths = self.get_files_in_directory()
        if not paths:
            raise EmptyDirectoryException
        for path in tqdm(paths, desc="Scanning files", mininterval=0.01, unit='files', miniters=1, smoothing=1):
            file = File(path)
            if file.extension in EXCLUDED_EXTENSIONS:
                continue
            if self.apply_filters(file):
                found.append(file)
        
        return found