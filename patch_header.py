import re

with open("frontend/src/pages/Database.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_header = """                                <div className="p-5 border-b border-gray-100 flex justify-between items-center bg-white/50">
                                <div>
                                    <h2 className="text-lg font-black text-gray-900 tracking-tight uppercase">Cluster: {activeTable.name}</h2>
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Primary Key: {activeTable.pk}</p>
                                </div>
                                <div className="text-[10px] font-black uppercase tracking-widest text-rose-500 bg-rose-50 px-3 py-1.5 rounded-lg border border-rose-100">
                                    Administrative Access Active
                                </div>
                            </div>"""

# Wait, let's use a regex to be safe about whitespace.
old_header_regex = r"<div className=\"p-5 border-b border-gray-100 flex justify-between items-center bg-white/50\">\s*<div>\s*<h2.*?Cluster: \{activeTable.name\}.*?</div>\s*<div className=\"text-\[10px\] font-black uppercase tracking-widest text-rose-500 bg-rose-50 px-3 py-1\.5 rounded-lg border border-rose-100\">\s*Administrative Access Active\s*</div>\s*</div>"

new_header = """<div className="p-5 border-b border-gray-100 flex justify-between items-center bg-white/50">
                                <div>
                                    <h2 className="text-lg font-black text-gray-900 tracking-tight uppercase">Cluster: {activeTable.name}</h2>
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Primary Key: {activeTable.pk}</p>
                                </div>
                                <div className="flex items-center space-x-3">
                                    {activeTable.name === 'plate_detections' && (
                                        <button onClick={handleDeleteAllRequest} className="px-4 py-2 bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5 flex items-center">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                            Delete All Data
                                        </button>
                                    )}
                                    <div className="text-[10px] font-black uppercase tracking-widest text-rose-500 bg-rose-50 px-3 py-2 rounded-xl border border-rose-100">
                                        Administrative Access Active
                                    </div>
                                </div>
                            </div>"""

content = re.sub(old_header_regex, new_header, content, flags=re.DOTALL)

with open("frontend/src/pages/Database.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected Delete All button into header!")
