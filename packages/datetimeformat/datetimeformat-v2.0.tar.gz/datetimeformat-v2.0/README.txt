#datetimeformat

##Description
```
1) Make educated guess of datetime format

2) Generate standardized datetime and timezone format given the timezone input
```

##Datetime format inferrer installation
```
pip install datetimeformat
```

### Input
```
from datetimeformat import inferrer

datetime_string =  '23/10/2020 13:13:59.59 +0900'
print(inferrer.guess_datetime_format(datetime_string)
```
### Output
```
"%d/%m/%Y %H:%M:%S.%f %z"
```

##Standardized datetime, timezone format

### Input
```
from datetimeformat import formatter

datetime_string =  '23/10/2020 13:13:59.59 +0900'
print(formatter.standardize_datetime_format(datetime_string='23/10/2020 13:13:59.59 +0900', datetime_format=False, timezone:str='Asia/Singapore', standardized_dt_format="%Y-%m-%d %H:%M:%S %z"))
```
### Output
```
"2020-10-23 12:13:59 +0800"
```

### To see available timezone options
```
import pytz
pytz.all_timezones
```
```
['Africa/Abidjan',
 'Africa/Accra',
 'Africa/Addis_Ababa',
 ...]
```