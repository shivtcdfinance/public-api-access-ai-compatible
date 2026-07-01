#!/usr/bin/env python3
"""Test: Validate api_canon JSON schema and trust ratings."""
import json, sys, os

errors = []

# Load the JSON
for fname in ['api_canon.min.json', 'api_canon.full.json']:
    if not os.path.exists(fname):
        errors.append(f"Missing: {fname}")
        continue
    with open(fname) as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get('apis', [])
    
    # Check required fields
    required = ['name', 'domain', 'url', 'trust', 'auth', 'https', 'cat']
    for i, e in enumerate(entries):
        for field in required:
            if field not in e:
                errors.append(f"{fname}[{i}]: missing field '{field}'")
    
    # Validate trust values
    valid_trust = {'trusted', 'likely_safe', 'marketplace', 'unknown', 'suspicious'}
    for i, e in enumerate(entries):
        if e.get('trust') not in valid_trust:
            errors.append(f"{fname}[{i}]: invalid trust '{e.get('trust')}'")
    
    # Validate auth values (common ones)
    valid_auth = {'no', 'apikey', 'oauth', 'x-mashape-key', 'rapidapi-key', 'user-agent', 'yes', 'all'}
    for i, e in enumerate(entries):
        if e.get('auth') not in valid_auth:
            errors.append(f"{fname}[{i}]: unusual auth '{e.get('auth')}'")
    
    # Check no suspicious domains snuck in as trusted
    suspicious_tlds = ['.xyz', '.cf', '.gq', '.ga', '.ml', '.tk']
    for i, e in enumerate(entries):
        if e.get('trust') == 'trusted':
            for tld in suspicious_tlds:
                if e.get('domain', '').endswith(tld):
                    errors.append(f"{fname}[{i}]: suspicious TLD {tld} marked as trusted")
    
    print(f"✅ {fname}: {len(entries)} entries, {len(errors) - (len(errors) - sum(1 for e in errors if fname in e))} errors")

if errors:
    print(f"\n❌ {len(errors)} validation errors:")
    for e in errors[:20]:
        print(f"  {e}")
    sys.exit(1)
else:
    print("\n✅ All validation checks passed!")
    sys.exit(0)
