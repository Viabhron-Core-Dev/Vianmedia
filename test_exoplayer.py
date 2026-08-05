import urllib.request
import re

url = "https://exoplayer.dev/doc/reference/androidx/media3/common/VideoSize.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    html = urllib.request.urlopen(req).read().decode("utf-8")
    print("Fetched ExoPlayer docs.")
    import textwrap
    lines = textwrap.wrap(re.sub(r'<[^>]+>', ' ', html), width=100)
    for i, line in enumerate(lines):
        if "unappliedRotationDegrees" in line:
            print("---")
            print("\n".join(lines[max(0, i-5):i+15]))
except Exception as e:
    print(e)
