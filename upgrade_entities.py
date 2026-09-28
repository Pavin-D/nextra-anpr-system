with open("tracking.html", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """                        <div className="flex flex-wrap gap-2">
                            {knownPlates.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold">Awaiting telemetry...</span>
                            ) : (
                                knownPlates.map((p, i) => (
                                    <button 
                                        key={i} 
                                        onClick={() => searchTrajectory(p)}
                                        className="px-3 py-1.5 bg-gray-50 border border-gray-100 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 text-xs text-gray-600 rounded-lg font-mono font-black shadow-sm transition-all transform hover:-translate-y-0.5">
                                        {p}
                                    </button>
                                ))
                            )}
                        </div>"""

new_block = """                        <div className="grid grid-cols-2 gap-3">
                            {knownPlates.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold col-span-2">Awaiting telemetry...</span>
                            ) : (
                                knownPlates.map((p, i) => (
                                    <button 
                                        key={i} 
                                        onClick={() => searchTrajectory(p)}
                                        style={{ animation: `fade-in 0.4s ease-out ${i * 0.05}s both` }}
                                        className="relative group flex items-center justify-between px-3.5 py-3 bg-white border border-gray-100 hover:border-indigo-300 rounded-xl font-mono shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden">
                                        <div className="absolute inset-0 bg-gradient-to-r from-indigo-50/0 via-indigo-50/70 to-indigo-100/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 ease-in-out z-0"></div>
                                        
                                        <div className="flex items-center space-x-2.5 relative z-10">
                                            <div className="w-1.5 h-1.5 rounded-full bg-slate-300 group-hover:bg-indigo-500 group-hover:shadow-[0_0_8px_rgba(99,102,241,0.8)] transition-all duration-300"></div>
                                            <span className="text-xs font-black text-gray-700 group-hover:text-indigo-700 transition-colors">{p}</span>
                                        </div>
                                        
                                        <div className="relative z-10 bg-gray-50 group-hover:bg-indigo-100 p-1.5 rounded-md transition-colors shadow-sm">
                                            <svg className="w-3 h-3 text-gray-400 group-hover:text-indigo-600 transform group-hover:translate-x-0.5 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M9 5l7 7-7 7"></path></svg>
                                        </div>
                                    </button>
                                ))
                            )}
                        </div>"""

content = content.replace(old_block, new_block)

with open("tracking.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Upgraded Active Network Entities UI!")
