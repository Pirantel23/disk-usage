import os
from datetime import datetime
from utils import Utils
import coloring as cl
from utils import Utils
import subprocess
import json

class File:
    def __init__(self, path: str, streamname: str) -> None:
        self.path = path
        self.extension = self.get_extension()
        self.creation_date = self.get_creation_date()
        self.size = self.get_size()
        self.nested_level = self.get_nested_level()
        self.author_uid = self.get_author_uid()
        self.ads_data = self.get_ads_data(streamname)
    
    def __repr__(self) -> str:
        return f'File: {self.path}\n{cl.MAGENTA}Size: {Utils.upscale_units(self.size)} {cl.CYAN}Creation Date: {self.creation_date}{cl.RESET}'

    @Utils.handle_file_errors
    def get_size(self) -> int: return os.path.getsize(self.path)
    
    @Utils.handle_file_errors
    def get_extension(self) -> str: return os.path.splitext(self.path)[-1]
    
    @Utils.handle_file_errors
    def get_creation_date(self) -> datetime: return datetime.fromtimestamp(os.path.getctime(self.path))
        
    @Utils.handle_file_errors
    def get_nested_level(self) -> int: return len(self.path.split(os.sep)) - 1
    
    @Utils.handle_file_errors
    def get_author_uid(self) -> int: return os.stat(self.path).st_uid

    @Utils.handle_file_errors
    def get_ads_data(self, stream_name: str = ':') -> dict:
        try:
            full_stream_path = f"{self.path}:{stream_name}"

            with open(full_stream_path, 'r') as stream_file:
                ads_data_raw = stream_file.read()

            ads_data = json.loads(ads_data_raw)
            return ads_data
        except Exception:
            return {}