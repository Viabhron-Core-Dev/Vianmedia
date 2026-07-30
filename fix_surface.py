with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_block = """                        factory = { ctx ->
                            PlayerView(ctx).apply {
                                player = exoPlayer
                                useController = true
                            }
                        },"""

new_block = """                        factory = { ctx ->
                            val view = android.view.LayoutInflater.from(ctx).inflate(com.example.R.layout.player_view_texture, null) as PlayerView
                            view.apply {
                                player = exoPlayer
                                useController = true
                            }
                        },"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced PlayerView with TextureView XML inflation")
else:
    print("Could not find block")
