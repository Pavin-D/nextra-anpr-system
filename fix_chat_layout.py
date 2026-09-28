import re

with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Root div
old_root = '<div className="relative w-full h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">'
new_root = '<div className="relative w-full h-[100dvh] sm:h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900 flex flex-col pt-10 px-6 pb-6">'
content = content.replace(old_root, new_root)

# 2. Update Navbar div
old_nav = '<div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">'
new_nav = '<div className="w-full z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all flex-shrink-0">'
content = content.replace(old_nav, new_nav)

# 3. Update Chat Window Wrapper
old_chat = """            {/* MAIN CHAT INTERFACE */}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex justify-center z-[900]">"""
new_chat = """            {/* MAIN CHAT INTERFACE */}
            <div className="flex-1 w-full mt-6 flex justify-center z-[900] min-h-0 relative">"""
content = content.replace(old_chat, new_chat)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Migrated chat.html to flex layout!")
