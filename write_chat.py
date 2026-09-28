import re

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract VoiceNav
voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', index_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

chat_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - AI Intelligence Chat</title>
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
        @keyframes fade-in-up {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .typing-dot {{ animation: typing 1.4s infinite ease-in-out both; }}
        .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
        .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}
        @keyframes typing {{ 0%, 80%, 100% {{ transform: scale(0); }} 40% {{ transform: scale(1); }} }}
        .msg-content strong {{ color: #4f46e5; font-weight: 900; background: rgba(79, 70, 229, 0.1); padding: 0 4px; border-radius: 4px; }}
        .msg-content ul {{ list-style-type: none; padding: 0; margin: 0; }}
        .msg-content li {{ margin-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 8px; position: relative; padding-left: 1.5rem; }}
        .msg-content li::before {{ content: "→"; position: absolute; left: 0; color: #4f46e5; font-weight: bold; }}
        .msg-content li:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans min-h-screen">
    <div id="root"></div>
    
    <script type="text/babel">
{voice_nav_code}

function ChatApp() {{
    const [messages, setMessages] = React.useState([]);
    const [input, setInput] = React.useState('');
    const [isTyping, setIsTyping] = React.useState(false);
    const messagesEndRef = React.useRef(null);

    React.useEffect(() => {{
        const saved = localStorage.getItem('nextra_chat_history');
        if (saved) {{
            setMessages(JSON.parse(saved));
        }} else {{
            setMessages([{{
                role: 'bot', 
                text: "Welcome to NEXTRA Intelligence Search.\\nI am deeply integrated into the surveillance grid. You can ask me:\\n- \\"Find vehicles from cam1 between 10 am and 2 pm\\"\\n- \\"Show me blacklisted threats spotted today\\"\\n- \\"Count detections yesterday at India Gate\\"\\n- \\"Did DL2CQ3150 pass any cameras recently?\\"\\n\\nHow can I assist your operation?"
            }}]);
        }}
    }}, []);

    React.useEffect(() => {{
        if(messages.length > 0) localStorage.setItem('nextra_chat_history', JSON.stringify(messages));
        messagesEndRef.current?.scrollIntoView({{ behavior: 'smooth' }});
    }}, [messages]);

    const handleSend = async (e) => {{
        e.preventDefault();
        if (!input.trim()) return;
        
        const userMsg = input.trim();
        setInput('');
        
        const newMessages = [...messages, {{ role: 'user', text: userMsg }}];
        setMessages(newMessages);
        setIsTyping(true);

        try {{
            const res = await fetch('/api/v1/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{ message: userMsg }})
            }});
            const data = await res.json();
            
            setIsTyping(false);
            setMessages([...newMessages, {{ role: 'bot', text: data.reply }}]);
        }} catch (e) {{
            setIsTyping(false);
            setMessages([...newMessages, {{ role: 'bot', text: "Error connecting to Intelligence Search Service." }}]);
        }}
    }};
    
    const clearChat = () => {{
        const initial = [{{
            role: 'bot', 
            text: "Memory wiped. Connection re-established. Ready for new queries."
        }}];
        setMessages(initial);
        localStorage.setItem('nextra_chat_history', JSON.stringify(initial));
    }}

    const formatMessage = (text) => {{
        const lines = text.split('\\n');
        const elements = [];
        let currentList = [];
        
        const flushList = () => {{
            if (currentList.length > 0) {{
                elements.push(<ul key={{`ul-${{elements.length}}`}} className="my-3 bg-gray-50 p-4 rounded-xl border border-gray-100 shadow-inner">{{currentList}}</ul>);
                currentList = [];
            }}
        }};
        
        lines.forEach((line, i) => {{
            const parts = line.split(/(\\**.*?\\**)/g).map((part, j) => {{
                if (part.startsWith('**') && part.endsWith('**')) {{
                    return <strong key={{j}}>{{part.slice(2, -2)}}</strong>;
                }}
                return part;
            }});
            
            if (line.trim().startsWith('- ')) {{
                currentList.push(<li key={{`li-${{i}}`}} className="text-sm font-medium text-gray-700">{{parts.slice(1)}}</li>);
            }} else {{
                flushList();
                if (line.trim() !== '') {{
                    elements.push(<p key={{`p-${{i}}`}} className="mb-3 text-sm leading-relaxed text-gray-800">{{parts}}</p>);
                }}
            }}
        }});
        flushList();
        return elements;
    }};

    return (
        <div className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">
            
            {{/* BACKGROUND ACCENTS */}}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {{/* FLOATING TOP NAVIGATION BAR */}}
            <div className="absolute top-6 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">
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
                        <a href="/chat" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    </div>
                </div>
            </div>

            {{/* MAIN CHAT INTERFACE */}}
            <div className="absolute top-28 left-0 right-0 bottom-6 flex justify-center z-[900]">
                <div className="w-full max-w-4xl h-full flex flex-col rounded-3xl bg-gradient-to-br from-indigo-500 via-cyan-400 to-fuchsia-500 p-[2px] shadow-[0_20px_50px_rgba(0,0,0,0.1)]">
                    <div className="w-full h-full bg-white/95 backdrop-blur-3xl flex flex-col rounded-[22px] overflow-hidden relative">
                        
                        {{/* Chat Header */}}
                        <div className="px-6 py-5 border-b border-gray-100 flex items-center justify-between bg-white/50 backdrop-blur-md z-10 flex-shrink-0">
                            <div>
                                <h2 className="text-lg font-black text-gray-900 tracking-tight flex items-center">
                                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 mr-2 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></span>
                                    Intelligence Core
                                </h2>
                                <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Natural Language Query Engine</p>
                            </div>
                            <button onClick={{clearChat}} className="text-[10px] font-black uppercase tracking-widest text-rose-500 hover:text-white border-2 border-rose-100 hover:border-rose-500 hover:bg-rose-500 px-4 py-2 rounded-xl transition-all shadow-sm">
                                Wipe Memory
                            </button>
                        </div>

                        {{/* Chat Messages */}}
                        <div className="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
                            {{messages.map((m, i) => (
                                <div key={{i}} className={{`flex ${{m.role === 'user' ? 'justify-end' : 'justify-start'}}`}} style={{{{animation: 'fade-in-up 0.4s ease-out both'}}}}>
                                    
                                    {{/* Bot Avatar */}}
                                    {{m.role === 'bot' && (
                                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center mr-3 mt-1 shadow-md">
                                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                        </div>
                                    )}}

                                    <div className={{`max-w-[75%] rounded-2xl px-5 py-4 shadow-sm msg-content ${{m.role === 'user' ? 'bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-tr-sm' : 'bg-white border border-gray-100 text-gray-800 rounded-tl-sm shadow-[0_4px_20px_rgba(0,0,0,0.03)]'}}`}}>
                                        {{m.role === 'user' ? <p className="text-sm font-medium text-white">{{m.text}}</p> : formatMessage(m.text)}}
                                    </div>

                                    {{/* User Avatar */}}
                                    {{m.role === 'user' && (
                                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center ml-3 mt-1 shadow-md border-2 border-white">
                                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                        </div>
                                    )}}
                                </div>
                            ))}}

                            {{isTyping && (
                                <div className="flex justify-start">
                                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center mr-3 shadow-md">
                                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                    </div>
                                    <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm px-5 py-4 flex items-center space-x-1.5 shadow-[0_4px_20px_rgba(0,0,0,0.03)]">
                                        <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                        <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                        <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                    </div>
                                </div>
                            )}}
                            <div ref={{messagesEndRef}} />
                        </div>

                        {{/* Chat Input */}}
                        <div className="p-4 bg-gray-50 border-t border-gray-100 z-10 flex-shrink-0">
                            <form onSubmit={{handleSend}} className="relative flex items-center">
                                <input type="text" value={{input}} onChange={{e => setInput(e.target.value)}}
                                       placeholder="Ask the intelligence core..." 
                                       className="w-full bg-white border-2 border-gray-200 focus:border-indigo-500 rounded-xl pl-5 pr-14 py-4 text-sm font-medium text-gray-800 shadow-inner outline-none transition-all placeholder-gray-400" />
                                <button type="submit" disabled={{isTyping}} 
                                        className="absolute right-2 bg-indigo-600 hover:bg-indigo-500 text-white p-2.5 rounded-lg transition-transform transform hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 shadow-md">
                                        <svg className="w-5 h-5 transform rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                                </button>
                            </form>
                            <p className="text-center text-[9px] font-bold text-gray-400 uppercase tracking-widest mt-3">Powered by NEXTRA AI &bull; Deep-Search Telemetry</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}}

class ErrorBoundary extends React.Component {{
    constructor(props) {{ super(props); this.state = {{ hasError: false, error: null }}; }}
    static getDerivedStateFromError(error) {{ return {{ hasError: true, error }}; }}
    render() {{ 
        if (this.state.hasError) return <div style={{{{color:'white', padding:'40px', background:'red'}}}}><h1>UI Crash!</h1><pre>{{this.state.error.toString()}}</pre></div>; 
        return this.props.children; 
    }}
}}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<ErrorBoundary><ChatApp /></ErrorBoundary>);
</script>
</body>
</html>"""

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(chat_html)

print("Rewrote chat.html successfully!")
