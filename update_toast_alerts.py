import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

toast_logic = """
            // TOAST LOGIC
            const [toastAlert, setToastAlert] = React.useState(null);
            const seenAlerts = React.useRef(new Set());
            
            React.useEffect(() => {
                if (alerts && alerts.length > 0) {
                    const latest = alerts[0];
                    if (!seenAlerts.current.has(latest.id)) {
                        if (seenAlerts.current.size > 0) {
                            setToastAlert(latest);
                            setTimeout(() => setToastAlert(null), 8000);
                        }
                        alerts.forEach(a => seenAlerts.current.add(a.id));
                    }
                }
            }, [alerts]);
"""

toast_ui = """
                    {/* TOAST NOTIFICATION */}
                    {toastAlert && (
                        <div className="absolute top-24 left-1/2 transform -translate-x-1/2 z-[9999] bg-white rounded-2xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] border-2 border-rose-500 overflow-hidden flex animate-bounce flex-col w-[450px]">
                            <div className="bg-rose-500 text-white px-4 py-2 font-black tracking-widest text-sm flex items-center justify-between">
                                <div className="flex items-center">
                                    <span className="w-2.5 h-2.5 bg-white rounded-full animate-ping mr-3"></span>
                                    THREAT DETECTED
                                </div>
                                <button onClick={() => setToastAlert(null)} className="text-white/80 hover:text-white">&times;</button>
                            </div>
                            <div className="p-5 flex">
                                <div className="mr-4 text-rose-500">
                                    <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                </div>
                                <div>
                                    <div className="text-xl font-black text-gray-900 font-mono tracking-wider mb-1">{toastAlert.plate_number}</div>
                                    <div className="text-sm font-bold text-rose-600 mb-2 uppercase tracking-wide">{toastAlert.alert_type}</div>
                                    <div className="text-xs text-gray-600 mb-2">{toastAlert.description}</div>
                                    <div className="inline-block bg-gray-100 text-gray-700 text-xs font-bold px-2 py-1 rounded">📍 {toastAlert.camera_id} @ {new Date(toastAlert.timestamp).toLocaleTimeString()}</div>
                                </div>
                            </div>
                        </div>
                    )}
"""

if "// TOAST LOGIC" not in content:
    content = content.replace("const [loading, setLoading] = React.useState(true);", "const [loading, setLoading] = React.useState(true);" + toast_logic)
    content = content.replace("{/* MAIN CONTENT */}", toast_ui + "\n                    {/* MAIN CONTENT */}")
    
    with open("alerts.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Toast logic injected into alerts.html")
else:
    print("Toast already exists")
