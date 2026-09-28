import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html", "database.html"]

logout_script = """
    <!-- SECURE LOGOUT MODAL -->
    <script>
        function triggerLogout() {
            const overlay = document.createElement('div');
            overlay.className = "fixed inset-0 z-[9999] bg-slate-900/40 backdrop-blur-md flex items-center justify-center";
            overlay.style.animation = "fadeIn 0.2s ease-out forwards";
            
            // Add keyframes if not exists
            if (!document.getElementById('logout-styles')) {
                const style = document.createElement('style');
                style.id = 'logout-styles';
                style.innerHTML = `@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } } @keyframes scaleUp { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }`;
                document.head.appendChild(style);
            }

            overlay.innerHTML = `
                <div class="bg-white/95 backdrop-blur-3xl border-2 border-rose-200 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.2)] max-w-sm w-full mx-4 text-center" style="animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;">
                    <div class="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mx-auto mb-5 border border-rose-100 shadow-inner">
                        <svg class="w-8 h-8 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                    </div>
                    <h2 class="text-xl font-black text-gray-900 tracking-tight mb-2">Terminate Session?</h2>
                    <p class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-8">Are you sure want to logout</p>
                    <div class="flex space-x-3">
                        <button onclick="document.body.removeChild(this.closest('.fixed'))" class="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200">Cancel</button>
                        <button onclick="localStorage.removeItem('nextra_token'); localStorage.removeItem('nextra_user'); window.location.href='/login'" class="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-500 hover:from-rose-600 hover:to-red-600 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Confirm Logout</button>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
    </script>
"""

logout_button = '\n                        <button onClick={triggerLogout} className="px-4 py-2 ml-2 flex items-center text-xs font-black uppercase tracking-wider rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>'

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. Inject the script before closing </body>
        if "triggerLogout" not in content:
            content = content.replace("</body>", logout_script + "</body>")
            
        # 2. Inject the button into the navbar after the Database link
        if ">Logout</button>" not in content:
            content = re.sub(
                r'(<a href="/database"[^>]*>Database</a>)',
                r'\1' + logout_button,
                content
            )
            
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Injected native glassmorphism logout modal into all pages!")
