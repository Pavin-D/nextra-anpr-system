with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# Revert to standard absolute layout to perfectly match all other pages
old_root = 'className="relative w-full h-[100dvh] overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900 flex flex-col px-6 pb-6 pt-12 space-y-6"'
new_root = 'className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900"'
content = content.replace(old_root, new_root)

# Navbar
old_nav = 'className="z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all flex-shrink-0 mt-[max(env(safe-area-inset-top),_0.5rem)]"'
new_nav = 'className="absolute top-6 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all"'
content = content.replace(old_nav, new_nav)

# Chat Box Wrapper
old_chat_wrapper = 'className="flex-1 flex justify-center z-[900] min-h-0"'
new_chat_wrapper = 'className="absolute top-28 left-6 right-6 bottom-6 flex justify-center z-[900]"'
content = content.replace(old_chat_wrapper, new_chat_wrapper)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Restored exact absolute alignment!")
