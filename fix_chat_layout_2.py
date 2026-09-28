with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Adjust height to dynamic viewport (100dvh) and add more top padding (pt-12) to clear the URL bar completely.
old_root_class = 'className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900 flex flex-col p-6 space-y-6"'
new_root_class = 'className="relative w-full h-[100dvh] overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900 flex flex-col px-6 pb-6 pt-12 space-y-6"'
content = content.replace(old_root_class, new_root_class)

# Fix 2: Increase chat box width from max-w-4xl to max-w-6xl
old_chat_width = 'className="w-full max-w-4xl h-full flex flex-col rounded-3xl'
new_chat_width = 'className="w-full max-w-7xl h-full flex flex-col rounded-3xl'
content = content.replace(old_chat_width, new_chat_width)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied layout fixes: pt-12, 100dvh, and max-w-7xl")
