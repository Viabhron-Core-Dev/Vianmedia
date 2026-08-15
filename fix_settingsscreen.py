import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Add to router
router_old = """            "main" -> MainSettingsMenu(
                onNavigate = { currentMenu = it },
                onNavigateBack = onNavigateBack
            )"""
router_new = """            "main" -> MainSettingsMenu(
                onNavigate = { currentMenu = it },
                onNavigateBack = onNavigateBack
            )
            "general" -> GeneralSettingsPage(onNavigateBack = { currentMenu = "main" })"""
content = content.replace(router_old, router_new)

# Add to MainSettingsMenu lazy column
menu_old = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {"""
menu_new = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            item {
                SettingsListItem(
                    icon = Icons.Filled.Palette,
                    title = "General",
                    subtitle = "Theme, typography, and appearance",
                    onClick = { onNavigate("general") }
                )
            }"""
content = content.replace(menu_old, menu_new)

# Add GeneralSettingsPage
general_page = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun GeneralSettingsPage(onNavigateBack: () -> Unit) {
    val context = LocalContext.current
    val settingsManager = remember { SettingsManager.getInstance(context) }
    val themePref by settingsManager.themePreference.collectAsState()
    val fontPref by settingsManager.fontPreference.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("General Settings") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            Text("Theme", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(8.dp))
            val themes = listOf("System Default", "Light", "Dark", "True Black")
            themes.forEach { theme ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { settingsManager.setThemePreference(theme) }
                        .padding(vertical = 8.dp)
                ) {
                    androidx.compose.material3.RadioButton(
                        selected = themePref == theme,
                        onClick = null
                    )
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(theme, style = MaterialTheme.typography.bodyLarge)
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            Text("Typography", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(8.dp))
            val fonts = listOf("Default", "Serif", "Monospace")
            fonts.forEach { font ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { settingsManager.setFontPreference(font) }
                        .padding(vertical = 8.dp)
                ) {
                    androidx.compose.material3.RadioButton(
                        selected = fontPref == font,
                        onClick = null
                    )
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(font, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}
"""

content = content + general_page

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)
