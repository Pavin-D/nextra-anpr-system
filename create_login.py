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
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden m-0 p-0 flex items-center justify-center">
    
    <!-- BACKGROUND ACCENTS -->
    <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-300/40 rounded-full blur-[120px] pointer-events-none"></div>
    <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-fuchsia-300/40 rounded-full blur-[120px] pointer-events-none"></div>

    <div id="root" class="z-10 w-full flex justify-center"></div>
    
    <script type="text/babel">
        function LoginApp() {
            const [username, setUsername] = React.useState("");
            const [password, setPassword] = React.useState("");
            const [error, setError] = React.useState("");
            const [loading, setLoading] = React.useState(false);

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
                    <div className="text-center mt-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">
                        Unauthorized access is strictly prohibited
                    </div>
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

print("Created login.html!")
