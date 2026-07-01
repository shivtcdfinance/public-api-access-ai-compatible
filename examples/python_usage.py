#!/usr/bin/env python3
"""API Canon — Python integration example.
Loads the API database, filters by trust + category, and calls a matching endpoint."""
import json, urllib.request, sys

# Load from local file or GitHub
try:
    with open('api_canon.min.json') as f:
        apis = json.load(f)
except FileNotFoundError:
    url = "https://raw.githubusercontent.com/shivtcdfinance/api-canon/main/api_canon.min.json"
    apis = json.loads(urllib.request.urlopen(url).read())

def find_api(keyword, trust='trusted', auth='no', https=True):
    """Find the best matching API for a keyword."""
    results = [a for a in apis
               if keyword.lower() in a.get('name','').lower()
               and a.get('trust') == trust
               and a.get('https') == https
               and a.get('auth') == auth]
    if not results:
        results = [a for a in apis
                   if keyword.lower() in a.get('cat','').lower()
                   and a.get('trust') == trust
                   and a.get('https')]
    return results[0] if results else None

# Example: find a weather API
api = find_api('weather')
if api:
    print(f"🏆 Best weather API: {api['name']}")
    print(f"   URL:  {api['url']}")
    print(f"   Auth: {api['auth']}")
    print(f"   Trust: {api['trust']}")
else:
    print("No match found")
