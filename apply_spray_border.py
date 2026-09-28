import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace Nav Bar
nav_old = """            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="absolute top-6 left-6 right-6 h-16 bg-white/80 backdrop-blur-2xl border border-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] flex items-center px-6 justify-between z-[1000] transition-all">"""
nav_new = """            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="absolute top-6 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.4)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">"""

content = content.replace(nav_old, nav_new)

# Add closing div for Nav Bar
# We look for the start of the next section
live_preview_start = "            {/* LIVE AI PREVIEW MODAL */}"
content = content.replace(live_preview_start, "                </div>\n            </div>\n\n" + live_preview_start)
# Wait, the original had one closing div for the nav bar (the outer one). Since we added a wrapper, we just add one MORE closing div.
# But I replaced the opening `<div ...>` with TWO opening `<div ...>`.
# So the original closing `</div>` is still there! I just need to add ONE more `</div>`.
# The original nav bar ends right before LIVE AI PREVIEW MODAL.
# Let's verify:
#             </div>
#
#             {/* LIVE AI PREVIEW MODAL */}
content = content.replace("            </div>\n\n            {/* LIVE AI PREVIEW MODAL */}", "                </div>\n            </div>\n\n            {/* LIVE AI PREVIEW MODAL */}")

# Replace Sidebar
sidebar_old = """            {/* FLOATING SIDEBAR */}
            <div className={`absolute top-28 left-6 bottom-6 w-[400px] max-w-[90vw] bg-white/80 backdrop-blur-3xl p-8 flex flex-col shadow-[0_20px_50px_rgba(0,0,0,0.1)] rounded-3xl border border-white z-[900] overflow-y-auto transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}`}>"""

sidebar_new = """            {/* FLOATING SIDEBAR */}
            <div className={`absolute top-28 left-6 bottom-6 w-[400px] max-w-[90vw] z-[900] rounded-3xl bg-gradient-to-br from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_30px_rgba(34,211,238,0.4)] transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}`}>
                <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-[22px] overflow-y-auto relative">"""
                
content = content.replace(sidebar_old, sidebar_new)

# Add closing div for Sidebar
# The sidebar ends before the final `</div>` of the map container, then `);`
# Original end:
#                 </div>
#             </div>
#         </div>
#     );
# }
end_old = """                </div>
            </div>
        </div>
    );
}"""
end_new = """                </div>
                </div>
            </div>
        </div>
    );
}"""
content = content.replace(end_old, end_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied vibrant spray gradient borders!")
