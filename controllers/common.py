from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo
import datetime as dt
import json
import urllib.request

def parse_datetime_to_utc( date_str, time_str, timezone ):
  date_arr = date_str.split("-")
  time_arr = time_str.replace(" ",":").split(":")
  yr = int(date_arr[0])
  mo = int(date_arr[1])
  dy = int(date_arr[2])
  if "am" in time_str.lower() and int(time_arr[0]) == 12:
    hr = 0
  elif "pm" in time_str.lower() and int(time_arr[0]) != 12:
    hr = int(time_arr[0]) + 12
  else:
    hr = int(time_arr[0])
  mi = int(time_arr[1])
  return dt.datetime(yr, mo, dy, hr, mi, 0, tzinfo=ZoneInfo(timezone)).astimezone(ZoneInfo("Etc/UTC"))


def http_request(url):
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  req = urllib.request.Request( url, data = None, headers = {'User-Agent': user_agent} )
  with urllib.request.urlopen(req) as response:
    return BeautifulSoup(response.read().decode('utf-8').replace("<!--","").replace("-->",""), "html.parser")


def json_request(url):
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  req = urllib.request.Request( url, data = None, headers = {'User-Agent': user_agent} )
  with urllib.request.urlopen(req) as response:
    return json.loads(response.read().decode('utf-8'))


def json_from_file(file_name):
  with open( file_name, 'r') as f:
    return json.load(f)


def get_data_stat(row, datastat, default=None, href=False):
  cell = row.select_one(f'td[data-stat={datastat}], th[data-stat={datastat}]')
  if cell:
    if href:
      try:
        return cell.select_one('a').get('href')
      except:
        return default
    else:
      try:
        return int(cell.text)
      except:
        return cell.text
  else:
    return default

