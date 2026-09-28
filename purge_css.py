import re
with open("frontend/src/index.css", "r", encoding="utf-8") as f:
    css = f.read()

# We will just write a brand new clean file
clean_css = """@import "tailwindcss";

.glass-panel { -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.95); }
.row-enter { animation: fade-in 0.3s ease-out forwards; }
@keyframes fade-in { 0% { opacity: 0; transform: translateY(-10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes scanline { 0% { transform: translateY(-100vh); } 100% { transform: translateY(100vh); } }
.radar-sweep { background: linear-gradient(transparent, rgba(99, 102, 241, 0.2), transparent); animation: scanline 3s linear infinite; }

/* Leaflet Overrides */
.leaflet-draw-toolbar a { color: #4f46e5 !important; background-color: white !important; border: 1px solid #e2e8f0 !important; }
.leaflet-draw-toolbar a:hover { background-color: #eef2ff !important; }
.leaflet-top { top: 100px !important; }
.leaflet-right { right: 30px !important; }

@keyframes fade-in-up {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.typing-dot {
    animation: typing 1.4s infinite ease-in-out both;
}
.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes typing {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
.msg-content strong { color: #4f46e5; font-weight: 900; background: rgba(79,70,229,0.1); padding: 0 4px; border-radius: 4px; }
.msg-content ul { list-style-type: none; padding: 0; margin: 0; }
.msg-content li { position: relative; padding-left: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 0.5rem; }
.msg-content li:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.msg-content li::before { content: '►'; position: absolute; left: 0; color: #4f46e5; font-weight: bold; }
.input-glow:focus-within { box-shadow: 0 0 35px rgba(99, 102, 241, 0.25); }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 10px; }
.animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
@keyframes gradient-xy {
    0%, 100% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
}
.animate-gradient-xy { background-size: 400% 400%; animation: gradient-xy 8s ease infinite; }
@keyframes text-glow {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.3)); }
    50% { filter: drop-shadow(0 0 40px rgba(255,255,255,0.8)) drop-shadow(0 0 80px rgba(255,255,255,0.5)); }
}
.animate-text-glow { animation: text-glow 4s ease-in-out infinite; }
@keyframes tracking-in {
    0% { letter-spacing: 0.5em; opacity: 0; filter: blur(12px); transform: scale(1.1); }
    100% { letter-spacing: -0.05em; opacity: 1; filter: blur(0); transform: scale(1); }
}
.animate-tracking-in { animation: tracking-in 1.5s cubic-bezier(0.215, 0.610, 0.355, 1.000) both; }
.animate-scanline { animation: scanline 4s linear infinite; }
@keyframes radar-ping {
    0% { transform: scale(0.5); opacity: 0.8; border-width: 4px; }
    100% { transform: scale(3.5); opacity: 0; border-width: 1px; }
}
.animate-radar-ping { animation: radar-ping 3s cubic-bezier(0.1, 0.5, 0.9, 1) infinite; }
@keyframes bracket-pulse {
    0%, 100% { opacity: 0.3; transform: scale(0.95); }
    50% { opacity: 1; transform: scale(1.05); border-color: white; }
}
.animate-bracket-pulse { animation: bracket-pulse 2s ease-in-out infinite; }
"""

with open("frontend/src/index.css", "w", encoding="utf-8") as f:
    f.write(clean_css)

print("Purged Vite default CSS logic!")
