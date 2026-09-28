import re

filepath = "frontend/src/pages/Dashboard.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add dragging state variables
state_vars = """    const [showLivePreview, setShowLivePreview] = React.useState(false);
    const [aiProgress, setAiProgress] = React.useState(0);
    const [liveImgUrl, setLiveImgUrl] = React.useState('');
    const [modalPos, setModalPos] = React.useState({ x: 0, y: 0 });
    const dragging = React.useRef(false);
    const dragOffset = React.useRef({ x: 0, y: 0 });"""

content = re.sub(
    r"const \[showLivePreview, setShowLivePreview\].*?const \[liveImgUrl, setLiveImgUrl\] = React\.useState\(''\);",
    state_vars, content, flags=re.DOTALL
)

# 2. Add global mouse listeners in useEffect
mouse_listeners = """
        const handleMove = (e) => {
            if (!dragging.current) return;
            setModalPos({ x: e.clientX - dragOffset.current.x, y: e.clientY - dragOffset.current.y });
        };
        const handleUp = () => { dragging.current = false; };
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', handleUp);"""

cleanup_listeners = """              document.removeEventListener('mousemove', handleMove);
              document.removeEventListener('mouseup', handleUp);
              if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; }"""

content = content.replace("if (!mapInstance.current && mapRef.current) {", mouse_listeners + "\n        if (!mapInstance.current && mapRef.current) {")
content = content.replace("if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; }", cleanup_listeners)

# 3. Fix fetchLiveProgress to set the image URL
old_fetch = """        const fetchLiveProgress = async () => {
            try {
                const res = await fetch('/api/v1/progress');
                const data = await res.json();
                setAiProgress(data.progress);
                if (data.latest_img) setLiveImgUrl('data:image/jpeg;base64,' + data.latest_img);
            } catch (e) {}
        };"""

new_fetch = """        const fetchLiveProgress = async () => {
            try {
                const res = await fetch('/api/v1/progress');
                const data = await res.json();
                setAiProgress(data.progress);
                setLiveImgUrl('/api/v1/live-frame?t=' + Date.now());
            } catch (e) {}
        };"""

content = content.replace(old_fetch, new_fetch)

# 4. Modify the JSX modal to use the transform and mousedown
old_modal = """            {/* LIVE AI PREVIEW MODAL */}
            {showLivePreview && (
                <div className="absolute top-32 right-6 w-96 bg-white/90 backdrop-blur-2xl border border-white rounded-3xl shadow-[0_30px_60px_rgba(0,0,0,0.15)] overflow-hidden z-[999] transition-all">
                    <div className="bg-gradient-to-r from-indigo-600 to-blue-500 px-5 py-3 flex justify-between items-center shadow-inner">
                        <h3 className="font-bold text-xs text-white tracking-widest uppercase">Live AI Engine</h3>"""

new_modal = """            {/* LIVE AI PREVIEW MODAL */}
            {showLivePreview && (
                <div 
                    style={{ transform: `translate(${modalPos.x}px, ${modalPos.y}px)` }}
                    className="fixed top-32 right-6 w-96 bg-white/90 backdrop-blur-2xl border border-white rounded-3xl shadow-[0_30px_60px_rgba(0,0,0,0.25)] overflow-hidden z-[999] animate-fade-in transition-shadow duration-300">
                    <div 
                        onMouseDown={(e) => {
                            dragging.current = true;
                            dragOffset.current = { x: e.clientX - modalPos.x, y: e.clientY - modalPos.y };
                        }}
                        className="bg-gradient-to-r from-indigo-600 to-blue-500 px-5 py-3 flex justify-between items-center shadow-inner cursor-move active:cursor-grabbing">
                        <div className="flex items-center">
                            <svg className="w-4 h-4 text-white mr-2 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                            <h3 className="font-bold text-xs text-white tracking-widest uppercase select-none">Live AI Engine</h3>
                        </div>"""

content = content.replace(old_modal, new_modal)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched Dashboard.jsx")
