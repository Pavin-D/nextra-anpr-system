import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', content, re.DOTALL)
if voice_nav_match:
    with open("voicenav.txt", "w", encoding="utf-8") as f:
        f.write(voice_nav_match.group(1))
    print("Extracted VoiceNav")
else:
    print("Could not find VoiceNav")
