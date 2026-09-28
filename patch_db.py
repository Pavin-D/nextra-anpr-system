import os
import re

filepath = "frontend/src/pages/Database.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state variable
state_var = """    const [showSidebar, setShowSidebar] = React.useState(true);
    const [deleteModal, setDeleteModal] = React.useState({ show: false, pkVal: null, table: null });"""
content = re.sub(r"const \[showSidebar, setShowSidebar\] = React\.useState\(true\);", state_var, content)

# 2. Replace handleDelete with handleDeleteRequest and executeDelete
old_delete_func = """    const handleDelete = async (pkVal) => {
        if (!confirm(`Are you sure you want to permanently delete record ${pkVal} from ${activeTable.name}?`)) return;
        
        try {
            const res = await fetch(`/api/v1/database/data/${activeTable.name}/${encodeURIComponent(pkVal)}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                // Refresh data
                handleTableSelect(activeTable);
                fetchTables(); // Refresh counts
            } else {
                alert("Failed to delete record: " + (data.error || "Unknown error"));
            }
        } catch (e) {
            console.error('Error deleting record', e);
        }
    };"""

new_delete_func = """    const handleDeleteRequest = (pkVal) => {
        setDeleteModal({ show: true, pkVal, table: activeTable.name });
    };

    const executeDelete = async () => {
        const { pkVal, table } = deleteModal;
        try {
            const res = await fetch(`/api/v1/database/data/${table}/${encodeURIComponent(pkVal)}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                handleTableSelect(activeTable);
                fetchTables();
                setDeleteModal({ show: false, pkVal: null, table: null });
            } else {
                alert("Failed to delete record: " + (data.error || "Unknown error"));
            }
        } catch (e) {
            console.error('Error deleting record', e);
        }
    };"""

content = content.replace(old_delete_func, new_delete_func)

# 3. Modify the delete button JSX
old_button = """                                                    <td className="px-4 py-3 text-right">
                                                        <button onClick={() => handleDelete(row[activeTable.pk])} 
                                                                className="text-[9px] font-black uppercase tracking-widest bg-white text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 px-3 py-1.5 rounded-lg transition-colors shadow-sm">
                                                            Delete
                                                        </button>
                                                    </td>"""

new_button = """                                                    <td className="px-4 py-3 text-right">
                                                        {activeTable.name !== 'cameras' && (
                                                            <button onClick={() => handleDeleteRequest(row[activeTable.pk])} 
                                                                    className="text-[9px] font-black uppercase tracking-widest bg-white text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 px-3 py-1.5 rounded-lg transition-colors shadow-sm">
                                                                Delete
                                                            </button>
                                                        )}
                                                    </td>"""

content = content.replace(old_button, new_button)

# 4. Inject Modal JSX
modal_jsx = """
            {/* CUSTOM DELETE CONFIRMATION MODAL */}
            {deleteModal.show && (
                <div className="fixed inset-0 z-[10000] bg-slate-900/40 backdrop-blur-md flex items-center justify-center animate-fade-in">
                    <div className="bg-white/95 backdrop-blur-3xl border-2 border-rose-100 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.2)] max-w-sm w-full mx-4 text-center transform scale-100 animate-fade-in">
                        <div className="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-rose-100 shadow-inner">
                            <svg className="w-8 h-8 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </div>
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight mb-2">Confirm Deletion</h2>
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">Target Cluster: <span className="text-rose-500">{deleteModal.table}</span></p>
                        <p className="text-xs font-medium text-gray-600 mb-8">Are you sure you want to permanently delete record <span className="font-black text-gray-900">#{deleteModal.pkVal}</span>? This action cannot be undone.</p>
                        <div className="flex space-x-3">
                            <button onClick={() => setDeleteModal({ show: false, pkVal: null, table: null })} className="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200 shadow-sm">Cancel</button>
                            <button onClick={executeDelete} className="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-500 hover:from-rose-600 hover:to-red-600 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Delete</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}"""

content = re.sub(r"\s*</div>\s*\);\s*}\s*$", modal_jsx, content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched Database.jsx")
