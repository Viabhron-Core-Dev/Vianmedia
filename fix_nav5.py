import re

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("""val popped = navController.popBackStack()
                        com.example.LogKeeper.log("popBackStack() returned $popped, current backstack size: ${navController.currentBackStack.value.size}", "Navigation")
                        if (!popped) {
                            com.example.LogKeeper.log("No backstack entry to pop — finishing Activity", "Navigation")
                            (context as? android.app.Activity)?.finish()
                        }""", """val popped = navController.popBackStack()
                        com.example.LogKeeper.log("popBackStack() returned $popped, current backstack size: ${navController.currentBackStack.value.size}", "Navigation")
                        if (!popped || (initialUris.isNotEmpty() && navController.currentDestination?.route == "main")) {
                            com.example.LogKeeper.log("No backstack entry to pop or launched via intent — finishing Activity", "Navigation")
                            (context as? android.app.Activity)?.finish()
                        }""")

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
print("Replaced back logic")
