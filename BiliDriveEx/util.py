# -*- coding: utf-8 -*-

import os
import sys
from os import path
import hashlib
import types
import requests
import json
import time
import tempfile

bundle_dir = tempfile.gettempdir()

size_string = lambda byte: f"{byte / 1024 / 1024 / 1024:.2f} GB" if byte > 1024 * 1024 * 1024 else f"{byte / 1024 / 1024:.2f} MB" if byte > 1024 * 1024 else f"{byte / 1024:.2f} KB" if byte > 1024 else f"{int(byte)} B"

def calc_sha1(data, hex=True):
    sha1 = hashlib.sha1()
    if hasattr(data, '__iter__') and \
       type(data) is not bytes:
        for chunk in data:
            sha1.update(chunk)
    else:
        sha1.update(data)
    return sha1.hexdigest() if hex else sha1.digest()
    
    
def image_download(url):
    headers = {
        'Referer': "http://t.bilibili.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    }
    content = []
    last_chunk_time = None
    try:
        for chunk in requests.get(url, headers=headers, timeout=10, stream=True).iter_content(128 * 1024):
            if last_chunk_time is not None and time.time() - last_chunk_time > 5:
                return None
            content.append(chunk)
            last_chunk_time = time.time()
        return b"".join(content)
    except:
        return None
    

def read_history():
    try:
        with open(path.join(bundle_dir, "history.json"), "r", encoding="utf-8") as f:
            history = json.loads(f.read())
    except:
        history = {}
    return history
    

def read_in_chunk(file_name, chunk_size=4 * 1024 * 1024, chunk_number=-1):
    chunk_counter = 0
    with open(file_name, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if data != b"" and (chunk_number == -1 or chunk_counter < chunk_number):
                yield data
                chunk_counter += 1
            else:
                return
                
def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")