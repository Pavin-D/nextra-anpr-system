import os
import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()
    
# 1. Update Left Column Border (Incident Log)
old_left = "bg-white/90 backdrop-blur-3xl rounded-[22px] shadow-sm border border-gray-100 overflow-hidden"
new_left = "bg-white/90 backdrop-blur-3xl rounded-[22px] border-2 border-rose-200/80 shadow-[0_0_20px_rgba(244,63,94,0.15)] overflow-hidden"
content = content.replace(old_left, new_left)

# 2. Update Right Column Dossier Border (Selected State)
old_right_sel = "bg-gradient-to-b from-rose-50 to-white rounded-[22px] shadow-sm border border-rose-100 overflow-hidden flex flex-col relative animate-fade-in"
new_right_sel = "bg-gradient-to-b from-rose-50 to-white rounded-[22px] border-2 border-rose-200/80 shadow-[0_0_20px_rgba(244,63,94,0.15)] overflow-hidden flex flex-col relative animate-fade-in"
content = content.replace(old_right_sel, new_right_sel)

# 3. Update Right Column Dossier Border (Empty State)
old_right_empty = "bg-white/40 backdrop-blur-md rounded-[22px] border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400"
new_right_empty = "bg-white/40 backdrop-blur-md rounded-[22px] border-2 border-dashed border-rose-200 flex flex-col items-center justify-center text-rose-300 shadow-[0_0_20px_rgba(244,63,94,0.05)]"
content = content.replace(old_right_empty, new_right_empty)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated borders on alerts.html to use customized Rose theme!")
