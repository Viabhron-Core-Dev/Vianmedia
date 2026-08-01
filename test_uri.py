import urllib.parse

uri1 = "content://media/external/video/media/1000000033"
encoded = "Y29udGVudDovL21lZGlhL2V4dGVybmFsL3ZpZGVvL21lZGlhLzEwMDAwMDAwMzM="
# wait, it's base64 encoded URL safe!
import base64
print(base64.urlsafe_b64decode(encoded).decode('utf-8'))
