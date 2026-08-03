from urllib.request import urlopen

try:
    html = urlopen("https://developer.android.com/reference/androidx/media3/common/VideoSize").read().decode('utf-8')
    if "unappliedRotationDegrees" in html:
        print("Found unappliedRotationDegrees in docs.")
    if "getUnappliedRotationDegrees" in html:
        print("Found getUnappliedRotationDegrees")
except Exception as e:
    print(e)
