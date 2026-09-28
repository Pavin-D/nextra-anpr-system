login_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Secure Authentication</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fade-in { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
        
        @keyframes gradient-xy {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        .animate-gradient-xy {
            background-size: 400% 400%;
            animation: gradient-xy 8s ease infinite;
        }

        @keyframes text-glow {
            0%, 100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.3)); }
            50% { filter: drop-shadow(0 0 40px rgba(255,255,255,0.8)) drop-shadow(0 0 80px rgba(255,255,255,0.5)); }
        }
        .animate-text-glow {
            animation: text-glow 4s ease-in-out infinite;
        }

        /* NEW HIGH-TECH ANIMATIONS */
        @keyframes tracking-in {
            0% { letter-spacing: 0.5em; opacity: 0; filter: blur(12px); transform: scale(1.1); }
            100% { letter-spacing: -0.05em; opacity: 1; filter: blur(0); transform: scale(1); }
        }
        .animate-tracking-in { animation: tracking-in 1.5s cubic-bezier(0.215, 0.610, 0.355, 1.000) both; }

        @keyframes scanline {
            0% { transform: translateY(-100vh); }
            100% { transform: translateY(100vh); }
        }
        .animate-scanline { animation: scanline 4s linear infinite; }

        @keyframes radar-ping {
            0% { transform: scale(0.5); opacity: 0.8; border-width: 4px; }
            100% { transform: scale(3.5); opacity: 0; border-width: 1px; }
        }
        .animate-radar-ping { animation: radar-ping 3s cubic-bezier(0.1, 0.5, 0.9, 1) infinite; }
        
        @keyframes bracket-pulse {
            0%, 100% { opacity: 0.3; transform: scale(0.95); }
            50% { opacity: 1; transform: scale(1.05); border-color: white; }
        }
        .animate-bracket-pulse { animation: bracket-pulse 2s ease-in-out infinite; }
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden m-0 p-0 flex items-center justify-center">
    
    <!-- BACKGROUND ACCENTS FOR LOGIN PAGE -->
    <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-300/40 rounded-full blur-[120px] pointer-events-none"></div>
    <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-fuchsia-300/40 rounded-full blur-[120px] pointer-events-none"></div>

    <div id="root" class="z-10 w-full flex justify-center h-full"></div>
    
    <script type="text/babel">
        function LoginApp() {
            const [username, setUsername] = React.useState("");
            const [password, setPassword] = React.useState("");
            const [error, setError] = React.useState("");
            const [loading, setLoading] = React.useState(false);
            
            // SPLASH SCREEN STATES
            const [showSplash, setShowSplash] = React.useState(true);
            const [isExiting, setIsExiting] = React.useState(false);

            const dismissSplash = () => {
                if(isExiting) return;
                setIsExiting(true);
                setTimeout(() => {
                    setShowSplash(false);
                }, 800);
            };

            const handleLogin = async (e) => {
                e.preventDefault();
                setError("");
                setLoading(true);
                try {
                    const res = await fetch("/api/v1/auth/login", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ username, password })
                    });
                    const data = await res.json();
                    
                    if (data.token) {
                        localStorage.setItem("nextra_token", data.token);
                        localStorage.setItem("nextra_user", data.username);
                        window.location.href = "/";
                    } else {
                        setError(data.error || "Authentication failed");
                    }
                } catch (err) {
                    setError("Network error. Please try again.");
                }
                setLoading(false);
            };

            return (
                <div className="w-full h-full flex items-center justify-center relative">
                    
                    {/* LOGIN FORM (Behind Splash) */}
                    <div className="w-full max-w-md animate-fade-in mx-4">
                        <div className="text-center mb-8">
                            <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                            <p className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mt-2">Central Security Command</p>
                        </div>

                        <div className="bg-white/80 backdrop-blur-xl border-2 border-indigo-100 rounded-3xl p-8 shadow-[0_20px_50px_rgba(99,102,241,0.15)] relative overflow-hidden">
                            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500"></div>
                            
                            <h2 className="text-xl font-black text-gray-900 tracking-tight mb-6 flex items-center">
                                <svg className="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                                Restricted Access
                            </h2>

                            {error && (
                                <div className="mb-6 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs font-bold text-rose-600 uppercase tracking-widest text-center">
                                    {error}
                                </div>
                            )}

                            <form onSubmit={handleLogin} className="space-y-5">
                                <div>
                                    <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Operator ID</label>
                                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required
                                        className="w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-indigo-400 focus:ring-0 bg-white/50 transition-colors text-sm font-bold text-gray-700 outline-none" 
                                        placeholder="Enter authorization ID" />
                                </div>
                                <div>
                                    <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Security Key</label>
                                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required
                                        className="w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-indigo-400 focus:ring-0 bg-white/50 transition-colors text-sm font-bold text-gray-700 outline-none" 
                                        placeholder="Enter security key" />
                                </div>
                                
                                <button type="submit" disabled={loading}
                                    className="w-full mt-4 bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-500 hover:to-blue-400 text-white font-black uppercase tracking-widest text-xs py-3.5 rounded-xl shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5 disabled:opacity-50">
                                    {loading ? "Authenticating..." : "Initialize Session"}
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* HIGH-TECH INTERACTIVE SPLASH SCREEN OVERLAY */}
                    {showSplash && (
                        <div 
                            onClick={dismissSplash}
                            className={`absolute inset-0 z-[10000] flex flex-col items-center justify-center bg-gradient-to-br from-indigo-600 via-fuchsia-600 to-cyan-500 animate-gradient-xy cursor-pointer overflow-hidden transition-all duration-[800ms] ease-in-out ${isExiting ? 'opacity-0 scale-105 filter blur-sm' : 'opacity-100 scale-100'}`}
                        >
                            {/* Surveillance Dot Grid Background */}
                            <div className="absolute inset-0 opacity-20 mix-blend-overlay" style={{backgroundImage: 'radial-gradient(white 1px, transparent 1px)', backgroundSize: '30px 30px'}}></div>
                            
                            {/* Sweeping Laser Scanline */}
                            <div className="absolute left-0 right-0 h-[2px] bg-white shadow-[0_0_15px_3px_rgba(255,255,255,0.8)] animate-scanline z-10 pointer-events-none opacity-50 mix-blend-overlay"></div>

                            {/* Expanding Radar Rings */}
                            <div className="absolute w-[200px] h-[200px] rounded-full border border-white/40 animate-radar-ping" style={{animationDelay: '0s'}}></div>
                            <div className="absolute w-[200px] h-[200px] rounded-full border border-white/40 animate-radar-ping" style={{animationDelay: '1.5s'}}></div>

                            {/* Center Logo Container */}
                            <div className="relative z-20 flex flex-col items-center justify-center">
                                
                                {/* Target Brackets */}
                                <div className="absolute -top-12 -left-12 w-12 h-12 border-t-4 border-l-4 border-white/50 rounded-tl-xl animate-bracket-pulse"></div>
                                <div className="absolute -top-12 -right-12 w-12 h-12 border-t-4 border-r-4 border-white/50 rounded-tr-xl animate-bracket-pulse"></div>
                                <div className="absolute -bottom-12 -left-12 w-12 h-12 border-b-4 border-l-4 border-white/50 rounded-bl-xl animate-bracket-pulse"></div>
                                <div className="absolute -bottom-12 -right-12 w-12 h-12 border-b-4 border-r-4 border-white/50 rounded-br-xl animate-bracket-pulse"></div>
                                
                                <h1 className="text-7xl md:text-[10rem] font-black text-white tracking-tighter animate-tracking-in animate-text-glow select-none">
                                    NEXTRA
                                </h1>
                            </div>

                            <div className="absolute bottom-16 flex flex-col items-center z-20 transition-all duration-300 transform hover:scale-110">
                                <p className="text-white font-black uppercase tracking-[0.4em] text-xs select-none animate-pulse drop-shadow-md">Biometric Lock Engaged</p>
                                <div className="flex items-center mt-3 bg-white/10 backdrop-blur-md px-6 py-2 rounded-full border border-white/20 shadow-[0_0_15px_rgba(255,255,255,0.1)]">
                                    <svg className="w-4 h-4 text-white mr-2 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 13l-3 3m0 0l-3-3m3 3V8m0 13a9 9 0 110-18 9 9 0 010 18z"></path></svg>
                                    <p className="text-white/90 font-bold uppercase tracking-[0.2em] text-[10px] select-none">Tap Screen To Initialize Override</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<LoginApp />);
    </script>
</body>
</html>"""

with open("login.html", "w", encoding="utf-8") as f:
    f.write(login_html)

print("Injected advanced hi-tech animations to splash screen!")
