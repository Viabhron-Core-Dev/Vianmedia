with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace("kotlinx.coroutines.flow.first(playlistRepo.allPlaylists)", "playlistRepo.allPlaylists.first()")
content = content.replace("kotlinx.coroutines.flow.first(playlistRepo.getItemsForPlaylist(tempPlaylistId))", "playlistRepo.getItemsForPlaylist(tempPlaylistId).first()")

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

content = content.replace("kotlinx.coroutines.flow.first(repo.allPlaylists)", "repo.allPlaylists.first()")

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
