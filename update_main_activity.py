import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

new_on_new_intent = """  override fun onNewIntent(intent: android.content.Intent?) {
      super.onNewIntent(intent)
      _currentIntent.value = intent
      if (intent?.action == "com.example.ACTION_START_PIP") {
          if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
              enterPictureInPictureMode(com.example.ui.screens.PipHelper.buildPipParams(this@MainActivity, com.example.service.PlayerManager.exoPlayer))
          }
      }
  }"""
content = re.sub(r'  override fun onNewIntent\(intent: android\.content\.Intent\?\) \{.*?\n  \}', new_on_new_intent, content, flags=re.DOTALL)

new_on_create = """    if (intent?.action == "com.example.ACTION_START_PIP") {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            enterPictureInPictureMode(com.example.ui.screens.PipHelper.buildPipParams(this@MainActivity, com.example.service.PlayerManager.exoPlayer))
        }
    }
    
    setContent {"""
content = content.replace("    setContent {", new_on_create)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
