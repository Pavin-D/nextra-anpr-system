with open("geofence.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Leaflet Controls Position (Hiding behind nav bar)
style_old = """        /* Restyle Leaflet Draw Controls for modern look */
        .leaflet-draw-toolbar a { background-color: #fff !important; color: #4f46e5 !important; border: 1px solid #e2e8f0 !important; }
        .leaflet-draw-toolbar a:hover { background-color: #eef2ff !important; }"""
        
style_new = """        /* Restyle Leaflet Draw Controls for modern look */
        .leaflet-draw-toolbar a { background-color: #fff !important; color: #4f46e5 !important; border: 1px solid #e2e8f0 !important; }
        .leaflet-draw-toolbar a:hover { background-color: #eef2ff !important; }
        /* Shift Leaflet controls down to clear the floating navbar */
        .leaflet-top { top: 100px !important; }
        .leaflet-right { right: 30px !important; }"""

content = content.replace(style_old, style_new)

# Fix Zone Detections Arrangement (Make it a compact 2-column grid instead of a tall list)
list_old = """                            <div className="space-y-3">
                                {detections.length === 0 ? (
                                    <div className="px-4 py-8 text-center text-gray-400 font-bold italic bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center">
                                        <svg className="w-8 h-8 mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                        No telemetry captured
                                    </div>
                                ) : (
                                    detections.map((d, i) => (
                                        <div key={i} className="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md hover:border-indigo-100 transition-all duration-300 group flex items-center justify-between" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                            <div>
                                                <div className="font-mono font-black text-cyan-500 tracking-wider text-sm mb-1 flex items-center">
                                                    {d.plate_number}
                                                </div>
                                                <div className="text-[10px] font-bold text-gray-400 flex items-center bg-gray-50 px-2 py-0.5 rounded border border-gray-100 w-max">
                                                    <svg className="w-3 h-3 mr-1 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                    {d.camera_id}
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-xs font-black text-gray-700 group-hover:text-indigo-900 transition-colors">
                                                    {new Date(d.timestamp).toLocaleTimeString(undefined, {timeStyle: 'short'})}
                                                </div>
                                                <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest">
                                                    {new Date(d.timestamp).toLocaleDateString(undefined, {dateStyle: 'medium'})}
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>"""

list_new = """                            <div className="grid grid-cols-2 gap-3 pb-4">
                                {detections.length === 0 ? (
                                    <div className="col-span-2 px-4 py-8 text-center text-gray-400 font-bold italic bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center">
                                        <svg className="w-8 h-8 mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                        No telemetry captured
                                    </div>
                                ) : (
                                    detections.map((d, i) => (
                                        <div key={i} className="bg-white border border-gray-100 rounded-xl p-3 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all duration-300 group flex flex-col justify-between transform hover:-translate-y-0.5" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                            <div className="flex justify-between items-start mb-3">
                                                <div className="font-mono font-black text-indigo-600 tracking-wider text-xs">
                                                    {d.plate_number}
                                                </div>
                                                <div className="text-[9px] font-black text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded flex items-center shadow-inner group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                                                    <svg className="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                    {d.camera_id}
                                                </div>
                                            </div>
                                            <div className="flex justify-between items-end border-t border-gray-50 pt-2 mt-auto">
                                                <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest">
                                                    {new Date(d.timestamp).toLocaleDateString(undefined, {dateStyle: 'short'})}
                                                </div>
                                                <div className="text-[10px] font-black text-gray-700 group-hover:text-indigo-900 transition-colors">
                                                    {new Date(d.timestamp).toLocaleTimeString(undefined, {timeStyle: 'short'})}
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>"""

content = content.replace(list_old, list_new)

with open("geofence.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed Leaflet controls & modernized detection layout!")
