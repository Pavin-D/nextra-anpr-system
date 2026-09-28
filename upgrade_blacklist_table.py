with open("blacklist.html", "r", encoding="utf-8") as f:
    content = f.read()

old_table = """                            <table className="w-full text-sm text-left">
                                <thead className="text-[10px] text-gray-400 uppercase tracking-widest sticky top-0 bg-white/95 backdrop-blur-xl z-10">
                                    <tr>
                                        <th className="px-6 py-4 rounded-tl-xl">Target Plate</th>
                                        <th className="px-6 py-4">Wanted Reason</th>
                                        <th className="px-6 py-4">Registry Date</th>
                                        <th className="px-6 py-4 text-right rounded-tr-xl">Action</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-50">
                                    {blacklist.length === 0 ? (
                                        <tr><td colSpan="4" className="px-6 py-12 text-center text-gray-400 font-bold italic bg-gray-50/50 rounded-xl">No active targets in network.</td></tr>
                                    ) : (
                                        blacklist.map((b, i) => (
                                            <tr key={i} className="hover:bg-gray-50/80 transition-colors group" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                                <td className="px-6 py-4 font-mono font-black text-gray-900 flex items-center">
                                                    <div className="w-2 h-2 rounded-full bg-rose-500 mr-3 shadow-[0_0_8px_rgba(244,63,94,0.6)]"></div>
                                                    {b.plate_number}
                                                </td>
                                                <td className="px-6 py-4 font-medium text-gray-600">{b.reason}</td>
                                                <td className="px-6 py-4 text-xs font-bold text-gray-400">{new Date(b.created_at).toLocaleString(undefined, {dateStyle: 'medium', timeStyle: 'short'})}</td>
                                                <td className="px-6 py-4 text-right">
                                                    <button onClick={() => handleDelete(b.plate_number)} className="text-gray-400 hover:text-rose-600 bg-white hover:bg-rose-50 px-4 py-2 rounded-lg text-xs font-black uppercase tracking-wider border-2 border-transparent hover:border-rose-100 shadow-sm transition-all transform hover:-translate-y-0.5">
                                                        Revoke
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>"""

new_table = """                            <table className="w-full text-sm text-left border-separate border-spacing-y-3">
                                <thead className="text-[10px] text-gray-400 uppercase tracking-widest sticky top-0 bg-white/95 backdrop-blur-xl z-20">
                                    <tr>
                                        <th className="px-6 py-2 font-black">Target Plate</th>
                                        <th className="px-6 py-2 font-black">Wanted Reason</th>
                                        <th className="px-6 py-2 font-black">Registry Date</th>
                                        <th className="px-6 py-2 text-right font-black">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {blacklist.length === 0 ? (
                                        <tr><td colSpan="4" className="px-6 py-12 text-center text-gray-400 font-bold italic bg-gray-50/80 rounded-2xl border-2 border-dashed border-gray-200">No active targets in network.</td></tr>
                                    ) : (
                                        blacklist.map((b, i) => (
                                            <tr key={i} className="bg-gray-50/50 hover:bg-white hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 group rounded-2xl" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                                <td className="px-6 py-4 rounded-l-2xl border-y border-l border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="inline-flex items-center px-4 py-1.5 bg-gray-900 border border-gray-700 rounded-lg shadow-inner group-hover:bg-gray-800 transition-colors">
                                                        <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse mr-2.5 shadow-[0_0_10px_rgba(244,63,94,1)]"></span>
                                                        <span className="font-mono font-black text-cyan-400 tracking-wider text-sm">{b.plate_number}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 border-y border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="flex items-start max-w-[250px]">
                                                        <svg className="w-4 h-4 text-rose-500 mr-2 mt-0.5 flex-shrink-0 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                                        <span className="font-bold text-gray-700 leading-snug group-hover:text-indigo-900 transition-colors">{b.reason}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 border-y border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="inline-flex items-center text-xs font-black text-gray-500 bg-gray-100 px-3 py-1.5 rounded-md border border-gray-200 group-hover:bg-indigo-50 group-hover:border-indigo-100 group-hover:text-indigo-600 transition-colors">
                                                        <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                                        {new Date(b.created_at).toLocaleString(undefined, {dateStyle: 'medium', timeStyle: 'short'})}
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 text-right rounded-r-2xl border-y border-r border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <button onClick={() => handleDelete(b.plate_number)} className="relative overflow-hidden inline-flex items-center justify-center bg-white border-2 border-gray-100 group-hover:border-rose-200 hover:!bg-rose-50 hover:!border-rose-300 text-gray-400 hover:!text-rose-600 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-0.5">
                                                        <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                                        Revoke
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>"""

content = content.replace(old_table, new_table)

with open("blacklist.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Upgraded Blacklist Table Rows!")
