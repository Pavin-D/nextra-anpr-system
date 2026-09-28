import re

with open("alerts.html", "r", encoding="utf-8") as f:
    alerts_content = f.read()

# Extract VoiceNav component
voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', alerts_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

database_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Database Management</title>
    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background-color: #cbd5e1; border-radius: 10px; }}
        @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(-5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-fade-in {{ animation: fade-in 0.3s ease-out forwards; }}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden m-0 p-0">
    <div id="root" class="h-full w-full"></div>
    
    <script type="text/babel">
{voice_nav_code}

function DatabaseApp() {{
    const [tables, setTables] = React.useState([]);
    const [activeTable, setActiveTable] = React.useState(null);
    const [tableData, setTableData] = React.useState([]);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {{
        fetchTables();
    }}, []);

    const fetchTables = async () => {{
        try {{
            const res = await fetch('/api/v1/database/tables');
            const data = await res.json();
            setTables(data.tables || []);
            if (data.tables && data.tables.length > 0 && !activeTable) {{
                handleTableSelect(data.tables[0]);
            }}
        }} catch (e) {{
            console.error('Error fetching tables');
        }}
        setLoading(false);
    }};

    const handleTableSelect = async (table) => {{
        setActiveTable(table);
        setLoading(true);
        try {{
            const res = await fetch(`/api/v1/database/data/${{table.name}}`);
            const data = await res.json();
            setTableData(data.rows || []);
        }} catch (e) {{
            console.error('Error fetching table data');
        }}
        setLoading(false);
    }};

    const handleDelete = async (pkVal) => {{
        if (!confirm(`Are you sure you want to permanently delete record ${{pkVal}} from ${{activeTable.name}}?`)) return;
        
        try {{
            const res = await fetch(`/api/v1/database/data/${{activeTable.name}}/${{encodeURIComponent(pkVal)}}`, {{ method: 'DELETE' }});
            const data = await res.json();
            if (data.success) {{
                // Refresh data
                handleTableSelect(activeTable);
                fetchTables(); // Refresh counts
            }} else {{
                alert("Failed to delete record: " + (data.error || "Unknown error"));
            }}
        }} catch (e) {{
            console.error('Error deleting record', e);
        }}
    }};

    return (
        <div className="relative w-full h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">
            {{/* BACKGROUND ACCENTS */}}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {{/* FLOATING TOP NAVIGATION BAR */}}
            <div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex space-x-2">
                        <a href="/" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                        <a href="/tracking" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                        <a href="/blacklist" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                        <a href="/geofence" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                        <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Alerts</a>
                        <a href="/database" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Database</a>
                    </div>
                </div>
            </div>

            {{/* MAIN CONTENT AREA */}}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {{/* LEFT COLUMN: TABLES LIST */}}
                <div className="w-64 flex-shrink-0 h-full flex flex-col bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md rounded-[22px] overflow-hidden">
                    <div className="p-5 border-b border-gray-100 bg-white/90">
                        <h2 className="text-sm font-black text-gray-900 uppercase tracking-widest">Data Clusters</h2>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white/50">
                        {{tables.map(table => (
                            <button key={{table.name}} onClick={{() => handleTableSelect(table)}} 
                                className={{`w-full text-left px-4 py-3 rounded-xl border transition-all ${{activeTable?.name === table.name ? 'bg-indigo-50 border-indigo-200 shadow-sm' : 'bg-white border-transparent hover:border-indigo-100 hover:shadow-sm'}}`}}>
                                <div className="text-xs font-black uppercase tracking-widest text-gray-800 mb-1">{{table.name}}</div>
                                <div className="text-[10px] font-bold text-indigo-500">{{table.count}} Records</div>
                            </button>
                        ))}}
                    </div>
                </div>

                {{/* RIGHT COLUMN: DATA VIEWER */}}
                <div className="flex-1 h-full flex flex-col bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md rounded-[22px] overflow-hidden">
                    {{activeTable ? (
                        <div className="w-full h-full flex flex-col bg-white/90">
                            <div className="p-5 border-b border-gray-100 flex justify-between items-center bg-white/50">
                                <div>
                                    <h2 className="text-lg font-black text-gray-900 tracking-tight uppercase">Cluster: {{activeTable.name}}</h2>
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Primary Key: {{activeTable.pk}}</p>
                                </div>
                                <div className="text-[10px] font-black uppercase tracking-widest text-rose-500 bg-rose-50 px-3 py-1.5 rounded-lg border border-rose-100">
                                    Administrative Access Active
                                </div>
                            </div>
                            
                            <div className="flex-1 overflow-auto custom-scrollbar p-0">
                                {{loading ? (
                                    <div className="flex justify-center items-center h-40">
                                        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                                    </div>
                                ) : tableData.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                                        <p className="font-bold uppercase tracking-widest text-xs">Cluster is empty</p>
                                    </div>
                                ) : (
                                    <table className="w-full text-left border-collapse">
                                        <thead className="bg-gray-50/80 sticky top-0 backdrop-blur-md border-b border-gray-200 z-10">
                                            <tr>
                                                {{Object.keys(tableData[0]).map(key => (
                                                    <th key={{key}} className="px-4 py-3 text-[10px] font-black uppercase tracking-widest text-gray-500 whitespace-nowrap">{{key}}</th>
                                                ))}}
                                                <th className="px-4 py-3 text-[10px] font-black uppercase tracking-widest text-rose-500 text-right">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {{tableData.map((row, i) => (
                                                <tr key={{i}} className="hover:bg-indigo-50/30 transition-colors animate-fade-in">
                                                    {{Object.keys(row).map(key => (
                                                        <td key={{key}} className="px-4 py-3 text-xs font-medium text-gray-700 whitespace-nowrap max-w-[200px] overflow-hidden text-ellipsis" title={{String(row[key])}}>
                                                            {{String(row[key])}}
                                                        </td>
                                                    ))}}
                                                    <td className="px-4 py-3 text-right">
                                                        <button onClick={{() => handleDelete(row[activeTable.pk])}} 
                                                                className="text-[9px] font-black uppercase tracking-widest bg-white text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 px-3 py-1.5 rounded-lg transition-colors shadow-sm">
                                                            Delete
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}}
                                        </tbody>
                                    </table>
                                )}}
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center bg-white/50 text-gray-400 text-xs font-bold uppercase tracking-widest">
                            Select a cluster to view records
                        </div>
                    )}}
                </div>
            </div>
        </div>
    );
}}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<DatabaseApp />);
    </script>
</body>
</html>
"""

with open("database.html", "w", encoding="utf-8") as f:
    f.write(database_html)

print("Created database.html!")
