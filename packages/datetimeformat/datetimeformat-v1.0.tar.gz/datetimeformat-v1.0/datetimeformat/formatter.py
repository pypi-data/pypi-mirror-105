from datetime import datetime
import pytz
from datetimeformat import inferrer

def standardize_datetime_format(datetime_string:str, datetime_format:bool=False, timezone:str='Asia/Singapore', standardized_dt_format:str="%Y-%m-%d %H:%M:%S %z") -> datetime:
    datetime_format = datetime_format if datetime_format else inferrer.guess_datetime_format(datetime_string)
    parsed_dt = datetime.strptime(datetime_string, datetime_format)
    standardized_dt = parsed_dt.astimezone(pytz.timezone(timezone)).strftime(standardized_dt_format)
    return standardized_dt
