import feedparser, json, os, urllib.request

SEARCH = "hololive serendipity"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]
STATE_FILE = "seen.json"
RSS_URL = f"https://nyaa.si/?page=rss&q={SEARCH.replace(' ', '+')}&c=0_0&f=0"

def load_seen():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f)), False
    return set(), True  # True = first run, don't spam old results

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen)[-500:], f)

def notify(title, link):
    req = urllib.request.Request(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=title.encode("utf-8"),
        headers={"Title": "New Nyaa torrent", "Click": link, "Tags": "cat"},
        method="POST",
    )
    urllib.request.urlopen(req)

def main():
    feed = feedparser.parse(RSS_URL)
    seen, first_run = load_seen()
    for entry in feed.entries:
        guid = entry.get("id") or entry.link
        if guid not in seen:
            if not first_run:
                notify(entry.title, entry.link)
            seen.add(guid)
    save_seen(seen)

if __name__ == "__main__":
    main()
