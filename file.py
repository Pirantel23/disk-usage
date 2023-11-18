import os
from datetime import datetime
from utils import Utils
import coloring as cl
from utils import Utils

class File:
    def __init__(self, path: str) -> None:
        self.path = path
        self.extension = self.get_extension()
        self.creation_date = self.get_creation_date()
        self.size = self.get_size()
        self.nested_level = self.get_nested_level()
        self.author_uid = self.get_author_uid()
    
    def __repr__(self) -> str:
        return f'File: {self.path}\n{cl.MAGENTA}Size: {Utils.upscale_units(self.size)} {cl.CYAN}Creation Date: {self.creation_date}{cl.RESET}'

    @Utils.handle_file_not_found_error
    def get_size(self) -> int: return os.path.getsize(self.path)
    
    @Utils.handle_file_not_found_error
    def get_extension(self) -> str: return os.path.splitext(self.path)[-1]
    
    @Utils.handle_file_not_found_error
    def get_creation_date(self) -> datetime: return datetime.fromtimestamp(os.path.getctime(self.path))
        
    @Utils.handle_file_not_found_error
    def get_nested_level(self) -> int: return len(self.path.split(os.sep)) - 1
    
    @Utils.handle_file_not_found_error
    def get_author_uid(self) -> int: return os.stat(self.path).st_uid