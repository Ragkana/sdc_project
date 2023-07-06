import subprocess as sp
from datetime import date, datetime, timedelta

today = date.today()
file_data = datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y-%m-%d')
sp.run(["/home/sdc/www/django_apps/myapp/daily_wrfdata/wf_temp/dataex_region_data_analysis.py -mt hres -r rainfall_daily_weighted_average -ai c6814b06-6555-444d-b123-13c6fea936ab -uf Province -o json -of /home/sdc/www/django_apps/myapp/daily_wrfdata/wf_temp/rf_"+file_data+"_cambodia.json"])
