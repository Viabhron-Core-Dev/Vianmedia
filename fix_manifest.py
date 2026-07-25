with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = """        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:supportsPictureInPicture="true"
            android:configChanges="screenSize|smallestScreenSize|screenLayout|orientation|uiMode|keyboard|keyboardHidden|colorMode|density"
            android:theme="@style/Theme.MyApplication">"""

replacement = """        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:launchMode="singleTask"
            android:supportsPictureInPicture="true"
            android:configChanges="screenSize|smallestScreenSize|screenLayout|orientation|uiMode|keyboard|keyboardHidden|colorMode|density"
            android:theme="@style/Theme.MyApplication">"""

content = content.replace(target, replacement)
with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
