import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

target = """                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Date</h4>
                                        <p className="text-sm font-bold text-gray-800">{new Date(selectedAlert.timestamp).toLocaleDateString()}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Time</h4>
                                        <p className="text-sm font-black text-indigo-600">{new Date(selectedAlert.timestamp).toLocaleTimeString()}</p>
                                    </div>
                                </div>"""

replacement = target + """
                                
                                {selectedAlert.blacklist_date && (
                                    <div className="bg-gray-50 border border-gray-100 rounded-xl p-4 flex items-center justify-between shadow-inner">
                                        <div>
                                            <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Blacklist Registry Date</h4>
                                            <p className="text-sm font-black text-gray-700">
                                                {new Date(selectedAlert.blacklist_date).toLocaleDateString()} 
                                                <span className="text-xs font-bold text-gray-400 ml-1">{new Date(selectedAlert.blacklist_date).toLocaleTimeString(undefined, {hour: '2-digit', minute:'2-digit'})}</span>
                                            </p>
                                        </div>
                                        <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-500 flex-shrink-0">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                                        </div>
                                    </div>
                                )}"""

content = content.replace(target, replacement)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added blacklist registry date to dossier successfully!")
