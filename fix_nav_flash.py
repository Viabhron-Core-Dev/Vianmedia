with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
"""    NavHost(navController = navController, startDestination = startDest) {""",
"""    val initialRoute = remember { intentDest ?: startDest }
    NavHost(navController = navController, startDestination = initialRoute) {""")

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
