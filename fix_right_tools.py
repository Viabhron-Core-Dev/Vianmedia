import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Replace all IconButton in RightTools with a smaller one
# It starts at: val RightTools: @Composable () -> Unit = {

def replace_right_tools(match):
    text = match.group(0)
    # We want to replace IconButton(...) { with IconButton(..., modifier = Modifier.size(32.dp)) {
    # and Icon(..., modifier = Modifier.size(18.dp))
    # It's better to just manually replace the specific lines
    
    # Just replace all `IconButton(onClick` with `IconButton(modifier = Modifier.size(36.dp), onClick` 
    # But ONLY inside RightTools
    # Wait, in RightTools there are multiple IconButtons. Let's just string replace the RightTools block.
    return text

# Actually, I can use a simpler replacement inside the RightTools block.
# Let's extract the RightTools block first.
start_idx = content.find("val RightTools: @Composable () -> Unit = {")
end_idx = content.find("Box(modifier = Modifier.align(Alignment.CenterEnd))", start_idx)

right_tools_block = content[start_idx:end_idx]

# Modify the IconButtons to be smaller
new_block = right_tools_block.replace('IconButton(onClick', 'IconButton(modifier = Modifier.size(36.dp), onClick')
new_block = new_block.replace('Icon(Icons.', 'Icon(modifier = Modifier.size(20.dp), imageVector = Icons.')
new_block = new_block.replace('Icon(\n                                        imageVector =', 'Icon(\n                                        modifier = Modifier.size(20.dp),\n                                        imageVector =')
new_block = new_block.replace('Icon(resizeIcon,', 'Icon(resizeIcon, modifier = Modifier.size(20.dp),')
new_block = new_block.replace('Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_playlist), contentDescription = "Minimize to Mini Player", tint = Color.White, modifier = Modifier.size(24.dp))', 'Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_playlist), contentDescription = "Minimize to Mini Player", tint = Color.White, modifier = Modifier.size(20.dp))')

content = content[:start_idx] + new_block + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
