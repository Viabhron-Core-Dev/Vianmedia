with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

content = content.replace("""        mediaSession?.run {
            player.release()
            release()
            mediaSession = null
        }""", """        mediaSession?.run {
            PlayerManager.release()
            release()
            mediaSession = null
        }""")

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
print("Replaced")
