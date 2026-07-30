import re

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = re.sub(
    r'\} else if \(settingsManager\.hasSeenWelcome\) "main" else "welcome"\n    \}\n *\n    androidx\.compose\.runtime\.LaunchedEffect\(initialUris, forceAction\) \{\n        if \(initialUris\.isNotEmpty\(\) && forceAction != null\) \{\n            navController\.navigate\(startDest\) \{\n                launchSingleTop = true\n                restoreState = true\n            \}\n        \}\n    \}',
    r"""} else null
    }

    androidx.compose.runtime.LaunchedEffect(intentDest) {
        if (intentDest != null) {
            navController.navigate(intentDest) {
                popUpTo(startDest) { inclusive = false }
                launchSingleTop = true
            }
        }
    }""",
    content,
    flags=re.MULTILINE
)

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
print("Replaced with regex")
