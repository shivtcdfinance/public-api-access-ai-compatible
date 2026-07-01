#!/usr/bin/env python3
"""Build script — rebuilds api_canon.json from upstream sources."""
import json, os, sys, re, urllib.request
from collections import defaultdict
from urllib.parse import urlparse

print("API Canon Builder")
print("=" * 60)

# Download upstream sources
sources = {
    'marcelscruz': 'https://raw.githubusercontent.com/marcelscruz/public-apis/main/db/resources.json',
    'public-api-lists': 'https://raw.githubusercontent.com/public-api-lists/public-api-lists/master/README.md',
}

# Trust classification (same as build_db.py)
TRUSTED = {'googleapis.com', 'google.com', 'microsoft.com', 'github.com', 'stripe.com', 'twilio.com',
           'openai.com', 'cohere.com', 'openweathermap.org', 'coinbase.com', 'ipinfo.io',
           'abstractapi.com', 'ip2location.com', 'alphavantage.co', 'twelvedata.com'}
SUSPICIOUS_TLDS = {'.xyz', '.cf', '.gq', '.ga', '.ml', '.tk', '.top', '.club', '.work', '.click'}
KNOWN_MARKETPLACES = {'rapidapi.com', 'apyhub.com'}

def classify(domain):
    domain = domain.lower()
    if domain in TRUSTED or any(domain.endswith('.'+t) for t in TRUSTED): return 'trusted'
    if domain in KNOWN_MARKETPLACES or any(domain.endswith('.'+m) for m in KNOWN_MARKETPLACES): return 'marketplace'
    if any(domain.endswith(g) for g in ['.gov','.edu','.mil','.gov.uk','.gov.in']): return 'trusted'
    if any(domain.endswith(p) for p in ['vercel.app','netlify.app','github.io','pages.dev','fly.dev']): return 'likely_safe'
    tld = '.' + domain.rsplit('.',1)[-1] if '.' in domain else ''
    if tld in SUSPICIOUS_TLDS: return 'suspicious'
    return 'unknown'

# Download marcelscruz
print("Downloading marcelscruz/public-apis...")
ms = json.loads(urllib.request.urlopen(sources['marcelscruz']).read())
ms_entries = ms.get('entries', ms) if isinstance(ms, dict) else ms
print(f"  Got {len(ms_entries)} entries")

# Build entries
apis = []
seen = set()

for e in ms_entries:
    url = e.get('Link', '')
    domain = 'unknown'
    if url:
        try:
            domain = urlparse(url).netloc.lower().replace('www.', '')
        except: pass
    auth = str(e.get('Auth', '')).lower()
    if auth in ('', 'no', 'none', 'false'): auth = 'no'
    
    entry = {
        'name': e.get('API', ''),
        'desc': e.get('Description', ''),
        'cat': (e.get('Category', '') or 'uncategorized').lower(),
        'domain': domain,
        'url': url,
        'auth': auth,
        'https': e.get('HTTPS') == True or str(e.get('HTTPS', '')).lower() in ('yes', 'true'),
        'cors': str(e.get('Cors', '')).lower(),
        'trust': classify(domain),
        'source': 'marcelscruz'
    }
    apis.append(entry)
    seen.add(domain)

# Build index for full version
index = {
    'by_category': defaultdict(list),
    'by_trust': defaultdict(list),
    'by_auth': defaultdict(list),
}
for i, a in enumerate(apis):
    index['by_category'][a['cat']].append(i)
    index['by_trust'][a['trust']].append(i)
    index['by_auth'][a['auth']].append(i)

# Write outputs
min_path = '../api_canon.min.json'
full_path = '../api_canon.full.json'

with open(min_path, 'w') as f:
    json.dump(apis, f, separators=(',', ':'))

index['by_category'] = {k: [apis[i]['name'] for i in v] for k, v in index['by_category'].items()}
index['by_trust'] = {k: [apis[i]['name'] for i in v] for k, v in index['by_trust'].items()}
index['by_auth'] = {k: [apis[i]['name'] for i in v] for k, v in index['by_auth'].items()}

full = {'metadata': {'total': len(apis), 'sources': ['marcelscruz/public-apis']}, 'apis': apis, 'index': index}
with open(full_path, 'w') as f:
    json.dump(full, f, indent=2)

print(f"\n✅ Built {min_path} ({os.path.getsize(min_path)//1024} KB)")
print(f"✅ Built {full_path} ({os.path.getsize(full_path)//1024} KB)")
print(f"   Total: {len(apis)} APIs")
