from exceptions import InvalidRangeOperator, InvalidSizeFormat
import subprocess

class Utils:
    def check_extension(file, extension: str) -> bool:
        return file.extension == extension
    
    def check_creation_date(file, date, range = None) -> bool:
        if range is None:
            return file.creation_date.date() == date.date()
        elif range == '+':
            return file.creation_date.date() >= date.date()
        elif range == '-':
            return file.creation_date.date() == date.date()
        else:
            raise InvalidRangeOperator
    
    def check_size(file, min_size: int, max_size: int):
        return file.size >= min_size and file.size <= max_size
    
    def check_nested_level(file, min_nested: int, max_nested: int):
        return file.nested_level >= min_nested and file.nested_level <= max_nested

    def downscale_units(size: str) -> int:
        size = size.lower()

        if size.isdigit():
            return int(size)

        units = {'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3, 'tb': 1024**4}

        for unit, multiplier in units.items():
            if size.endswith(unit) and size[:-len(unit)].strip().isdigit():
                return int(size[:-len(unit)].strip()) * multiplier

        raise InvalidSizeFormat

    def upscale_units(size: int):
        unit_number = 0
        while size >= 1024:
            size/=1024
            unit_number += 1

        return f"{size:.2f}{['B', 'KB', 'MB', 'GB', 'TB'][unit_number]}"

    def get_total_size(files) -> int:
        total = sum(file.size for file in files)
        return Utils.upscale_units(total)
    
    def get_all_users() -> list[str]:
        pass