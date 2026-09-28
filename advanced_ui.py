import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add a cool scanning animation keyframes to the <style> block
style_injection = """
        .glass-panel { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        .row-enter { animation: fade-in 0.3s ease-out forwards; }
        @keyframes fade-in { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes scanline { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
        .radar-sweep { background: linear-gradient(to bottom, transparent, rgba(99,102,241,0.2), transparent); animation: scanline 3s linear infinite; }
"""
content = re.sub(r'<style>.*?</style>', f'<style>{style_injection}</style>', content, flags=re.DOTALL)

# Modify Sidebar header to include a radar ping
header_replace = """<h2 className="text-3xl font-black text-gray-900 tracking-tight mb-1">Analytics</h2>"""
header_new = """<div className="flex items-center justify-between mb-1">
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight">Analytics</h2>
                                <div className="relative flex items-center justify-center w-8 h-8">
                                    <span className="absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-30 animate-ping"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.8)]"></span>
                                </div>
                            </div>"""
content = content.replace(header_replace, header_new)

# Modify OCR card to have the scanning line
ocr_replace = """<div className="bg-gradient-to-br from-white to-gray-50 p-5 rounded-2xl border border-gray-100 shadow-[0_8px_20px_rgba(0,0,0,0.03)] flex flex-col justify-center relative overflow-hidden group">"""
ocr_new = """<div className="bg-gradient-to-br from-white to-gray-50 p-5 rounded-2xl border border-indigo-50 shadow-[0_10px_30px_rgba(99,102,241,0.08)] flex flex-col justify-center relative overflow-hidden group">
                                    <div className="absolute inset-0 radar-sweep pointer-events-none"></div>"""
content = content.replace(ocr_replace, ocr_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Injected advanced UI animations")
