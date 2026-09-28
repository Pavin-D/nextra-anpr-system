import re

with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add CSS for input glow
style_old = "</style>"
style_new = """        .input-glow:focus-within { box-shadow: 0 0 35px rgba(99, 102, 241, 0.25); }
    </style>"""
content = content.replace(style_old, style_new)

# Replace Search Box
old_search_box = """                        {/* Chat Input */}
                        <div className="p-4 bg-gray-50 border-t border-gray-100 z-10 flex-shrink-0">
                            <form onSubmit={handleSend} className="relative flex items-center">
                                <input type="text" value={input} onChange={e => setInput(e.target.value)}
                                       placeholder="Ask the intelligence core..." 
                                       className="w-full bg-white border-2 border-gray-200 focus:border-indigo-500 rounded-xl pl-5 pr-14 py-4 text-sm font-medium text-gray-800 shadow-inner outline-none transition-all placeholder-gray-400" />
                                <button type="submit" disabled={isTyping} 
                                        className="absolute right-2 bg-indigo-600 hover:bg-indigo-500 text-white p-2.5 rounded-lg transition-transform transform hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 shadow-md">
                                        <svg className="w-5 h-5 transform rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                                </button>
                            </form>
                            <p className="text-center text-[9px] font-bold text-gray-400 uppercase tracking-widest mt-3">Powered by NEXTRA AI &bull; Deep-Search Telemetry</p>
                        </div>"""

new_search_box = """                        {/* Chat Input */}
                        <div className="p-6 bg-white/70 backdrop-blur-2xl border-t border-gray-100 z-10 flex-shrink-0 relative overflow-visible">
                            <form onSubmit={handleSend} className="relative flex items-center group max-w-5xl mx-auto input-glow rounded-[1.25rem] transition-shadow duration-500 z-20">
                                {/* Animated Ambient Glow Behind Input */}
                                <div className={`absolute -inset-1.5 bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 rounded-[1.5rem] blur-lg transition duration-700 opacity-20 ${input.trim() ? 'opacity-40 animate-pulse' : 'group-hover:opacity-30'}`}></div>
                                
                                <div className="relative w-full flex items-center bg-white rounded-[1.25rem] border-2 border-gray-100 group-hover:border-indigo-200 focus-within:border-indigo-400 transition-all duration-300">
                                    {/* Search Indicator Dot */}
                                    <div className="absolute left-6 flex items-center justify-center pointer-events-none">
                                        <div className="relative flex h-3.5 w-3.5">
                                          <span className={`absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75 ${input.trim() ? 'animate-ping' : ''}`}></span>
                                          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-indigo-500"></span>
                                        </div>
                                    </div>

                                    <input type="text" value={input} onChange={e => setInput(e.target.value)}
                                           placeholder="Enter target plate, timestamp, or camera node..." 
                                           className="w-full bg-transparent rounded-[1.25rem] pl-14 pr-16 py-4 text-[15px] font-bold text-gray-800 outline-none transition-all placeholder-gray-400" />
                                    
                                    <button type="submit" disabled={isTyping || !input.trim()} 
                                            className="absolute right-2.5 bg-gradient-to-r from-indigo-600 to-blue-500 text-white w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-300 transform hover:scale-110 disabled:opacity-40 disabled:hover:scale-100 shadow-[0_0_20px_rgba(79,70,229,0.4)] disabled:shadow-none overflow-hidden group/btn">
                                            <svg className={`w-5 h-5 transform transition-transform duration-300 ${input.trim() ? '-rotate-45 group-hover/btn:translate-x-1 group-hover/btn:-translate-y-1' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                                    </button>
                                </div>
                            </form>
                            
                            <p className="text-center text-[10px] font-black text-gray-400 uppercase tracking-widest mt-5 flex items-center justify-center space-x-3">
                                <span>Powered by NEXTRA AI</span>
                                <span className="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>
                                <span className="text-indigo-400 flex items-center">
                                    <svg className="w-3 h-3 mr-1 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    Deep-Search Telemetry Active
                                </span>
                            </p>
                        </div>"""

content = content.replace(old_search_box, new_search_box)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Upgraded search box with ultra-premium animations!")
