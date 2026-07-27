with open("app/src/main/java/com/example/service/PlayerManager.kt", "r") as f:
    content = f.read()

content = content.replace("val repo = com.example.data.PlaylistRepository(db.playlistDao())", "val dao = db.playlistDao()")
content = content.replace("repo.getAllPlaylistsSync()", "dao.getAllPlaylistsSync()")
content = content.replace("repo.deletePlaylistById(temp.id)", "dao.deletePlaylistById(temp.id)")

with open("app/src/main/java/com/example/service/PlayerManager.kt", "w") as f:
    f.write(content)
