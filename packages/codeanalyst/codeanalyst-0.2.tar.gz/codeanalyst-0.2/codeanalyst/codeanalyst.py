import requests
import json
from . import api

url = api

def codetest(code, lang, langv, cid = "2c1d7916a28c2ac644a6acb7abdf8847", secret = "36a72c45e217e3097fded87023f138722beaedc1b345ad50e3f7094ff9145548"):
  if langv is None:
    langv = 3
  jsun = {
    "clientId": cid,
    "clientSecret": secret,
    "script": code,
    "language": lang,
    "versionIndex": langv}
  req = requests.post(url, json = jsun)
  result = json.loads(req.text)
  return CodeAnalystResult(result)


class CodeAnalystResult:
  def __init__(self, result):
    self.result = result
