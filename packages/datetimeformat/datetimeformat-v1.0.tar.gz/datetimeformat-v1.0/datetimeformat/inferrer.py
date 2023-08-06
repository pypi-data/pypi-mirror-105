from datetime import datetime
from itertools import permutations 

class Utils:
    @staticmethod
    def get_all_datetime_formats() -> list:
        b = ['%d','%b','%Y']
        B = ['%d','%B','%Y']
        m = ['%d','%m','%Y']
        date_connectors = ['-','/',' ']
        all_possible_date_formats = []
        for date_connector in date_connectors:
            for date_formats in [b,B,m]:
                for date_format in list(permutations(date_formats)):
                    all_possible_date_formats += [date_connector.join(date_format)]
        time_formats = ['%H:%M %p', '%H:%M %p %z', '%H:%M %p %Z','%H:%M', '%H:%M:%S', '%H:%M:%S %z', '%H:%M:%S %Z', '%H:%M:%S.%f', '%H:%M:%S.%f %z', '%H:%M:%S.%f %Z']
        datetime_connectors = [' ',':']
        all_datetime_formats = []
        for datetime_connector in datetime_connectors:
            print(date_connector)
            for time_format in time_formats:
                for date_format in all_possible_date_formats:
                    all_datetime_formats += [date_format+datetime_connector+time_format]
        return all_datetime_formats
    
    @staticmethod
    def check_for_brackets(datetimestring: str, datetime_format: str) -> str:
        if '[' in datetimestring:
            datetime_format = '['+datetime_format+']'
        elif '<' in datetimestring:
            datetime_format = '<'+datetime_format+'>'
        elif '(' in datetimestring:
            datetime_format = '('+datetime_format+')'
        else:
            return datetime_format


def guess_datetime_format(datetimestring: str) -> str:
    datetime_formats = Utils.get_all_datetime_formats()
    for datetime_format in datetime_formats:
        try:
            datetime_format = Utils.check_for_brackets(datetimestring, datetime_format)
            datetime.strptime(datetimestring, datetime_format)
            return datetime_format
        except:
            continue
    return False
