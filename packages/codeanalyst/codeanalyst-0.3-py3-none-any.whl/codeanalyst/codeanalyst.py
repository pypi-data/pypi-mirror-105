import requests
import json
from . import api
from data import *
url = api

def codetest(code, lang, langv = None, cid = "2c1d7916a28c2ac644a6acb7abdf8847", secret = "36a72c45e217e3097fded87023f138722beaedc1b345ad50e3f7094ff9145548"):
  if langv is None and lang in v3_langs:
    langv = 3
  elif langv is None and lang in v2_langs:
    langv = 2
  elif langv is None and lang in v1_langs:
    langv = 1
  elif langv is None and lang in v0_langs:
    langv = 0
  
  if lang.lower() not in languages:
    raise CompilerError("Unknown language.")
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

class CompilerError(Exception):
    pass
