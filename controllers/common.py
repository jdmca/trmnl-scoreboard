from bs4 import BeautifulSoup
import urllib.request

def http_request(url):
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  req = urllib.request.Request( url, data = None, headers = {'User-Agent': user_agent} )
  with urllib.request.urlopen(req) as response:
    return BeautifulSoup(response.read().decode('utf-8').replace("<!--","").replace("-->",""), "html.parser")

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