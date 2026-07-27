with open("app/src/main/java/com/example/service/PlayerManager.kt", "r") as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.launch\npackage com.example.service", "package com.example.service\nimport kotlinx.coroutines.launch")

with open("app/src/main/java/com/example/service/PlayerManager.kt", "w") as f:
    f.write(content)
