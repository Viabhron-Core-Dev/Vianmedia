import re
with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Make startDest purely local to the LaunchedEffect (or keep it but make startDestination fixed)
# Let's change the startDestination of NavHost to be fixed: `if (settingsManager.hasSeenWelcome) "main" else "welcome"`

replacement1 = """    val startDest = if (settingsManager.hasSeenWelcome) "main" else "welcome"
    
    val intentDest = remember(initialUris, forceAction) {
        if (initialUris.isNotEmpty()) {"""

content = content.replace("    val startDest = remember(initialUris, forceAction) {\n        if (initialUris.isNotEmpty()) {", replacement1)

replacement2 = """        } else null
    }
        
    androidx.compose.runtime.LaunchedEffect(intentDest) {
        if (intentDest != null) {
            navController.navigate(intentDest) {
                popUpTo(navController.graph.id) { inclusive = true }
                launchSingleTop = true
            }
        }
    }"""

# We need to find the end of intentDest block and replace the old LaunchedEffect
content = re.sub(r'        } else if \(settingsManager\.hasSeenWelcome\) "main" else "welcome"\n    \}\n        \n    androidx\.compose\.runtime\.LaunchedEffect\(initialUris, forceAction\) \{\n        if \(initialUris\.isNotEmpty\(\) && forceAction != null\) \{\n            navController\.navigate\(startDest\) \{\n                launchSingleTop = true\n                restoreState = true\n            \}\n        \}\n    \}', replacement2, content, flags=re.MULTILINE)

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
print("Replaced")
