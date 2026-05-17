# Auto-Update from Keiyoshi (SFW Filtered)

This fork of keiyoshi/extensions automatically pulls updates from the original repository, but **only includes**:
- All SFW sources (`nsfw: 0`)
- Explicitly whitelisted NSFW sources

## How It Works

1. **Weekly Trigger**: GitHub Actions runs every Monday at 00:00 UTC
2. **Fetch**: Downloads the latest `index.json` from [keiyoshi/extensions](https://github.com/keiyoushi/extensions)
3. **Filter**: Removes all NSFW sources except those in the whitelist
4. **Update**: Commits and pushes changes to this repository

## Managing the NSFW Whitelist

Edit `nsfw-whitelist.json` to control which NSFW sources are included:

```json
{
  "description": "NSFW sources that are explicitly whitelisted for inclusion",
  "whitelist": [
    "Tachiyomi: Weeb Central",
    "Tachiyomi: Another NSFW Source"
  ]
}
```

### To Add a Whitelisted NSFW Source:

1. Find the source name from the original keiyoshi `index.json` (field: `"name"`)
2. Add it to the `whitelist` array in `nsfw-whitelist.json`
3. Commit and push
4. The next weekly update (or manual trigger) will include it

## Manual Updates

To trigger an update immediately without waiting for the weekly schedule:

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Weekly Update from Keiyoshi**
4. Click **Run workflow**

## Statistics

**Current Setup** (as of last update):
- Total entries: 602
- SFW sources: 601
- Whitelisted NSFW sources: 1 (Weeb Central)
- NSFW sources excluded: 1,392

## Notes

- The script automatically runs on push, so you can test it locally with: `python3 update-index.py`
- Both `index.json` and `index.min.json` are updated
- Git commits are only created if there are actual changes
- Uses GitHub's built-in permissions for secure commits
