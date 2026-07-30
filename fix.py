with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()
if "player.release()" in content:
    content = content.replace("player.release()", "PlayerManager.release()")
    with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
        f.write(content)
    print("Replaced")
