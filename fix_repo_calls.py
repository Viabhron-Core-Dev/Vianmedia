with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace("playlistRepo.getAllPlaylists()", "playlistRepo.allPlaylists")
content = content.replace("playlistRepo.deletePlaylistItem(it)", "playlistRepo.deletePlaylistItemById(it.id)")
content = content.replace(",\n                                displayName = item.mediaMetadata.title.toString()", "")

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

content = content.replace("repo.getAllPlaylists()", "repo.allPlaylists")
content = content.replace("repo.deletePlaylist(it)", "repo.deletePlaylistById(it.id)")

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

content = content.replace("repository.updatePlaylist(playlist!!.copy(name = newName))", "repository.updatePlaylists(listOf(playlist!!.copy(name = newName)))")

with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
