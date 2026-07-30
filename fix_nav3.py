with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_block = """        } else if (settingsManager.hasSeenWelcome) "main" else "welcome"
    }
        
    androidx.compose.runtime.LaunchedEffect(initialUris, forceAction) {
        if (initialUris.isNotEmpty() && forceAction != null) {
            navController.navigate(startDest) {
                launchSingleTop = true
                restoreState = true
            }
        }
    }"""

new_block = """        } else null
    }
        
    androidx.compose.runtime.LaunchedEffect(intentDest) {
        if (intentDest != null) {
            navController.navigate(intentDest) {
                popUpTo(startDest) { inclusive = false }
                launchSingleTop = true
            }
        }
    }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
    print("Replaced old_block")
else:
    print("old_block not found")
