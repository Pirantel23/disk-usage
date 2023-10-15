from datetime import datetime

class Analyser:
    def check_extension(file, extension: str) -> bool:
        return file.extension == extension
    
    def check_creation_date(file, date: datetime) -> bool:
        return file.creation_date.date() == date.date()
    
    def check_between_dates(file, date1: datetime, date2: datetime) -> bool:
        if date1.date() == date2.date():
            return Analyser.check_creation_date(file, date1)
        elif date1 > date2:
            return file.creation_date > date2 and file.creation_date < date1
        else:
            return file.creation_date > date1 and file.creation_date < date2