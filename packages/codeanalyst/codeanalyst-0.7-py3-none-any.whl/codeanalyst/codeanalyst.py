import requests
import json
from . import api
import aiohttp
from codeanalyst.data import *
url = api
session = aiohttp.ClientSession()

async def codetest(code, lang, langv = "None", cid = "2c1d7916a28c2ac644a6acb7abdf8847", secret = "36a72c45e217e3097fded87023f138722beaedc1b345ad50e3f7094ff9145548"):
  
  if lang.lower() not in languages:
    raise CompilerError("Unknown language.")

  if langv == "None" and lang in v3_langs:
    langv = 3
  elif langv == "None" and lang in v2_langs:
    langv = 2
  elif langv == "None" and lang in v1_langs:
    langv = 1
  elif langv == "None" and lang in v0_langs:
    langv = 0
  
  
  jsun = {
    "clientId": cid,
    "clientSecret": secret,
    "script": code,
    "language": languages.get(lang),
    "versionIndex": langv}
  async with session.post(url, json = jsun) as req:
    result = json.loads(await req.text())
  return CodeAnalystResult(result)


class CodeAnalystResult:
  def __init__(self, result):
    self.result = result

class CompilerError(Exception):
    pass
