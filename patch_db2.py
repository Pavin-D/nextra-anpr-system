import re

with open("frontend/src/pages/Database.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Hide cameras
content = content.replace("setTables(data.tables || []);", "setTables(data.tables ? data.tables.filter(t => t.name !== 'cameras') : []);")

# 2. Add deleteAllModal state
content = content.replace("const [deleteModal, setDeleteModal] = React.useState({ show: false, pkVal: null, table: null });", "const [deleteModal, setDeleteModal] = React.useState({ show: false, pkVal: null, table: null });\n    const [deleteAllModal, setDeleteAllModal] = React.useState(false);")

# 3. Add executeDeleteAll
delete_all_funcs = """    const handleDeleteAllRequest = () => { setDeleteAllModal(true); };
    const executeDeleteAll = async () => {
        try {
            const res = await fetch(`/api/v1/database/clear/${activeTable.name}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                handleTableSelect(activeTable);
                fetchTables();
                setDeleteAllModal(false);
            } else { alert("Failed to clear table: " + (data.error || "Unknown error")); }
        } catch (e) { console.error('Error clearing table', e); }
    };"""
content = content.replace("const handleDeleteRequest = (pkVal) => {", delete_all_funcs + "\n\n    const handleDeleteRequest = (pkVal) => {")

# 4. Add Delete All button in header
header_btn_old = """                                    <button onClick={() => {fetchTables(); if(activeTable) handleTableSelect(activeTable);}} 
                                            className="px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-xl font-black text-[10px] uppercase tracking-widest transition-colors flex items-center shadow-sm">
                                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                                        Refresh Data
                                    </button>"""
header_btn_new = """                                    {activeTable.name === 'plate_detections' && (
                                        <button onClick={handleDeleteAllRequest} className="px-4 py-2 bg-rose-50 hover:bg-rose-500 text-rose-500 hover:text-white border border-rose-200 hover:border-rose-500 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm flex items-center">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                            Delete All
                                        </button>
                                    )}
                                    <button onClick={() => {fetchTables(); if(activeTable) handleTableSelect(activeTable);}} 
                                            className="px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-xl font-black text-[10px] uppercase tracking-widest transition-colors flex items-center shadow-sm">
                                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                                        Refresh Data
                                    </button>"""
content = content.replace(header_btn_old, header_btn_new)

# 5. Add deleteAllModal JSX
modal_jsx = """            {deleteAllModal && (
                <div className="fixed inset-0 z-[10000] bg-slate-900/40 backdrop-blur-md flex items-center justify-center animate-fade-in">
                    <div className="bg-white/95 backdrop-blur-3xl border-2 border-rose-500 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] max-w-sm w-full mx-4 text-center transform scale-100 animate-fade-in">
                        <div className="w-16 h-16 bg-rose-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-rose-500/30">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        </div>
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight mb-2">NUKE CLUSTER</h2>
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">Target: <span className="text-rose-500">{activeTable?.name}</span></p>
                        <p className="text-xs font-medium text-gray-600 mb-8">Are you absolutely sure you want to annihilate ALL records in this cluster? This is irreversible.</p>
                        <div className="flex space-x-3">
                            <button onClick={() => setDeleteAllModal(false)} className="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200 shadow-sm">Cancel</button>
                            <button onClick={executeDeleteAll} className="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Wipe Data</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}"""
content = re.sub(r"\s*</div>\s*\);\s*}\s*$", "\n" + modal_jsx, content)

with open("frontend/src/pages/Database.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Frontend patched")
