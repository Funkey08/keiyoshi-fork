#!/usr/bin/env python3
"""
Auto-update script for keiyoshi-fork to pull only SFW sources and whitelisted NSFW sources.
This script fetches the latest index.json from keiyoshi/extensions and filters it.
"""

import json
import urllib.request
import sys
from pathlib import Path

KEIYOSHI_REPO = "https://raw.githubusercontent.com/keiyoushi/extensions/main"
INDEX_URL = f"{KEIYOSHI_REPO}/index.json"
SCRIPT_DIR = Path(__file__).parent

def load_whitelist():
    """Load NSFW whitelist from nsfw-whitelist.json"""
    whitelist_file = SCRIPT_DIR / "nsfw-whitelist.json"
    try:
        with open(whitelist_file) as f:
            data = json.load(f)
            return set(data.get("whitelist", []))
    except Exception as e:
        print(f"Warning: Could not load whitelist: {e}")
        return set()

def fetch_original_index():
    """Fetch the original index.json from keiyoshi/extensions"""
    try:
        print(f"Fetching original index from {INDEX_URL}...")
        with urllib.request.urlopen(INDEX_URL, timeout=30) as response:
            data = json.loads(response.read().decode())
        print(f"✓ Successfully fetched {len(data)} entries from keiyoshi")
        return data
    except Exception as e:
        print(f"✗ Error fetching original index: {e}")
        sys.exit(1)

def filter_entries(entries, whitelist):
    """
    Filter entries to keep only:
    - SFW sources (nsfw: 0)
    - NSFW sources in the whitelist
    """
    filtered = []
    nsfw_count = 0
    sfw_count = 0
    whitelisted_count = 0
    
    for entry in entries:
        name = entry.get("name", "")
        nsfw = entry.get("nsfw", 0)
        
        if nsfw == 0:
            # Keep all SFW sources
            filtered.append(entry)
            sfw_count += 1
        elif name in whitelist:
            # Keep whitelisted NSFW sources
            filtered.append(entry)
            whitelisted_count += 1
        else:
            # Skip other NSFW sources
            nsfw_count += 1
    
    print(f"\nFiltering results:")
    print(f"  SFW sources kept: {sfw_count}")
    print(f"  Whitelisted NSFW sources kept: {whitelisted_count}")
    print(f"  NSFW sources removed: {nsfw_count}")
    print(f"  Total entries after filtering: {len(filtered)}")
    
    return filtered

def save_index(entries):
    """Save filtered entries to index.json and index.min.json"""
    index_file = SCRIPT_DIR / "index.json"
    index_min_file = SCRIPT_DIR / "index.min.json"
    
    try:
        # Save pretty-printed version
        with open(index_file, 'w') as f:
            json.dump(entries, f, indent=4)
        print(f"✓ Updated {index_file}")
        
        # Save minified version
        with open(index_min_file, 'w') as f:
            json.dump(entries, f, separators=(',', ':'))
        print(f"✓ Updated {index_min_file}")
        
        return True
    except Exception as e:
        print(f"✗ Error saving index files: {e}")
        return False

def main():
    print("=" * 60)
    print("Keiyoshi Extensions Auto-Update (SFW + Whitelisted)")
    print("=" * 60)
    
    # Load whitelist
    whitelist = load_whitelist()
    print(f"\nWhitelisted NSFW sources: {whitelist}")
    
    # Fetch original index
    original_entries = fetch_original_index()
    
    # Filter entries
    filtered_entries = filter_entries(original_entries, whitelist)
    
    # Save results
    if save_index(filtered_entries):
        print("\n✓ Update completed successfully!")
        return 0
    else:
        print("\n✗ Update failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
