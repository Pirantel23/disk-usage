class Utils:
    def check_extension(file, extension: str) -> bool:
        return file.extension == extension
    
    def check_creation_date(file, date) -> bool:
        return file.creation_date.date() == date.date()
    
    def scale_units(size: int):
        unit_number = 0
        while size >= 1024:
            size/=1024
            unit_number += 1

        return f"{size}{['b', 'KB', 'MB', 'GB', 'TB'][unit_number]}"

    def get_total_size(files) -> int:
        total = sum(file.size for file in files)
        return Utils.scale_units(total)

    def check_between_dates(file, date1, date2) -> bool:
        if date1.date() == date2.date():
            return Utils.check_creation_date(file, date1)
        elif date1 > date2:
            return file.creation_date > date2 and file.creation_date < date1
        else:
            return file.creation_date > date1 and file.creation_date < date2