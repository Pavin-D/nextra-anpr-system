with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace Chat Header
old_header = """                        {/* Chat Header */}
                        <div className="px-6 py-5 border-b border-gray-100 flex items-center justify-between bg-white/50 backdrop-blur-md z-10 flex-shrink-0">
                            <div>
                                <h2 className="text-lg font-black text-gray-900 tracking-tight flex items-center">
                                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 mr-2 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></span>
                                    Intelligence Core
                                </h2>
                                <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Natural Language Query Engine</p>
                            </div>
                            <button onClick={clearChat} className="text-[10px] font-black uppercase tracking-widest text-rose-500 hover:text-white border-2 border-rose-100 hover:border-rose-500 hover:bg-rose-500 px-4 py-2 rounded-xl transition-all shadow-sm">
                                Wipe Memory
                            </button>
                        </div>

                        {/* Chat Messages */}
                        <div className="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">"""

new_header = """                        {/* Floating Action */}
                        <button onClick={clearChat} className="absolute top-4 right-6 z-[50] text-[10px] font-black uppercase tracking-widest text-rose-500 hover:text-white border-2 border-rose-100 hover:border-rose-500 hover:bg-rose-500 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-xl transition-all shadow-sm">
                            Wipe Memory
                        </button>

                        {/* Chat Messages */}
                        <div className="flex-1 overflow-y-auto p-6 pt-12 custom-scrollbar space-y-6">"""

content = content.replace(old_header, new_header)

# 2. Modify Chat Input Footer
old_footer = """                        {/* Chat Input */}
                        <div className="p-6 bg-white/70 backdrop-blur-2xl border-t border-gray-100 z-10 flex-shrink-0 relative overflow-visible">"""

new_footer = """                        {/* Chat Input */}
                        <div className="p-6 pb-4 z-10 flex-shrink-0 relative overflow-visible bg-transparent">"""

content = content.replace(old_footer, new_footer)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied UI floating tweaks!")
