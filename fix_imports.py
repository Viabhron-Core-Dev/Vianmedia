def fix_file(path):
    with open(path, "r") as f:
        content = f.read()
    
    if content.startswith("import kotlinx.coroutines.flow.first\n"):
        content = content.replace("import kotlinx.coroutines.flow.first\n", "", 1)
        # Find package declaration
        pkg_idx = content.find("package ")
        if pkg_idx != -1:
            end_pkg = content.find("\n", pkg_idx)
            if end_pkg != -1:
                content = content[:end_pkg+1] + "import kotlinx.coroutines.flow.first\n" + content[end_pkg+1:]
        
        with open(path, "w") as f:
            f.write(content)

fix_file("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt")
fix_file("app/src/main/java/com/example/ui/screens/PlayerScreen.kt")
