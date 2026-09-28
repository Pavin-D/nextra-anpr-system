import React, { useState, useEffect, useRef } from 'react';

const VoiceNav = () => {
            const [isActive, setIsActive] = React.useState(false);
            const [isProcessing, setIsProcessing] = React.useState(false);
            const activeRef = React.useRef(false);
            const recognitionRef = React.useRef(null);

            const toggleListening = () => {
                if (activeRef.current) {
                    activeRef.current = false;
                    setIsActive(false);
                    if(recognitionRef.current) recognitionRef.current.stop();
                    return;
                }

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Voice Navigation is not supported in this browser.");
                    return;
                }

                activeRef.current = true;
                setIsActive(true);
                
                const recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onresult = (event) => {
                    const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
                    console.log("Heard:", transcript);
                    
                    const wakeWords = ["hey next", "hey extra", "a next", "hey nex", "an extra"];
                    const isWakeWord = wakeWords.some(w => transcript.includes(w));
                    
                    if (isWakeWord) {
                        setIsProcessing(true);
                        setTimeout(() => setIsProcessing(false), 2000);
                        
                        if (transcript.includes("dashboard") || transcript.includes("overview") || transcript.includes("home")) window.location.href = "/";
                        else if (transcript.includes("tracking") || transcript.includes("track")) window.location.href = "/tracking";
                        else if (transcript.includes("blacklist") || transcript.includes("black list")) window.location.href = "/blacklist";
                        else if (transcript.includes("geofence") || transcript.includes("geo fence")) window.location.href = "/geofence";
                        else if (transcript.includes("chat") || transcript.includes("search")) window.location.href = "/chat";
                    }
                };

                recognition.onend = () => {
                    if (activeRef.current) {
                        try { recognition.start(); } catch(e) {}
                    }
                };

                recognitionRef.current = recognition;
                recognition.start();
            };

            return (
                <div className="flex items-center space-x-3 ml-4">
                    <button onClick={toggleListening} title="Toggle Always-On Voice Assistant" 
                            className={`p-2 rounded-full border transition-all ${isActive ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-sm' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-950'}`}>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                    </button>
                    {isActive && (
                        <span className={`text-[10px] font-bold uppercase tracking-widest ${isProcessing ? 'text-rose-500 animate-pulse' : 'text-cyan-400 animate-pulse'}`}>
                            {isProcessing ? 'Command Received' : 'Listening...'}
                        </span>
                    )}
                </div>
            );
        };

function ChatApp() {
    const [messages, setMessages] = React.useState([]);
    const [input, setInput] = React.useState('');
    const [isTyping, setIsTyping] = React.useState(false);
    const messagesEndRef = React.useRef(null);

    React.useEffect(() => {
        const saved = localStorage.getItem('nextra_chat_history');
        if (saved) {
            setMessages(JSON.parse(saved));
        } else {
            setMessages([{
                role: 'bot', 
                text: "Welcome to NEXTRA Intelligence Search.\nI am deeply integrated into the surveillance grid. You can ask me:\n- \"Find vehicles from cam1 between 10 am and 2 pm\"\n- \"Show me blacklisted threats spotted today\"\n- \"Count detections yesterday at India Gate\"\n- \"Did DL2CQ3150 pass any cameras recently?\"\n\nHow can I assist your operation?"
            }]);
        }
    }, []);

    React.useEffect(() => {
        if(messages.length > 0) localStorage.setItem('nextra_chat_history', JSON.stringify(messages));
        if (messagesEndRef.current && messagesEndRef.current.parentElement) {
            messagesEndRef.current.parentElement.scrollTo({
                top: messagesEndRef.current.parentElement.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        
        const userMsg = input.trim();
        setInput('');
        
        const newMessages = [...messages, { role: 'user', text: userMsg }];
        setMessages(newMessages);
        setIsTyping(true);

        try {
            await new Promise(r => setTimeout(r, 800));
            const data = { reply: "This is only the frontend dashboard hosted on Vercel. To run live AI queries, you need to connect to the active backend database and GPU server!" };
            
            setIsTyping(false);
            setMessages([...newMessages, { role: 'bot', text: data.reply }]);
        } catch (e) {
            setIsTyping(false);
            setMessages([...newMessages, { role: 'bot', text: "Error connecting to Intelligence Search Service." }]);
        }
    };
    
    const clearChat = () => {
        const initial = [{
            role: 'bot', 
            text: "Memory wiped. Connection re-established. Ready for new queries."
        }];
        setMessages(initial);
        localStorage.setItem('nextra_chat_history', JSON.stringify(initial));
    }

    const formatMessage = (text) => { return <p className="mb-3 text-sm leading-relaxed text-gray-800">{text}</p>; };
        
        lines.forEach((line, i) => {
            const parts = line.split(/(\**.*?\**)/g).map((part, j) => {
                if (part.startsWith('**') && part.endsWith('**')) {
                    return <strong key={j}>{part.slice(2, -2)}</strong>;
                }
                return part;
            });
            
            if (line.trim().startsWith('- ')) {
                currentList.push(<li key={`li-${i}`} className="text-sm font-medium text-gray-700">{parts.slice(1)}</li>);
            } else {
                flushList();
                if (line.trim() !== '') {
                    elements.push(<p key={`p-${i}`} className="mb-3 text-sm leading-relaxed text-gray-800">{parts}</p>);
                }
            }
        });
        flushList();
        return elements;
    };

    return (
        <div className="relative w-full h-[100dvh] sm:h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900 flex flex-col pt-10 px-6 pb-6">
            
            {/* BACKGROUND ACCENTS */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="w-full z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all flex-shrink-0">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex items-center space-x-1 lg:space-x-2 ml-auto">
                    <a href="/" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
                </div>
            </div>

            {/* MAIN CHAT INTERFACE */}
            <div className="flex-1 w-full mt-6 flex justify-center z-[900] min-h-0 relative">
                <div className="w-full max-w-7xl h-full flex flex-col rounded-3xl bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md overflow-hidden p-0">
                    <div className="w-full h-full bg-white/95 backdrop-blur-3xl flex flex-col rounded-none overflow-hidden relative">
                        
                        {/* Floating Action */}
                        <button onClick={clearChat} className="absolute top-4 right-6 z-[50] text-[10px] font-black uppercase tracking-widest text-rose-500 hover:text-white border-2 border-rose-100 hover:border-rose-500 hover:bg-rose-500 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-xl transition-all shadow-sm">
                            Wipe Memory
                        </button>

                        {/* Chat Messages */}
                        <div className="flex-1 overflow-y-auto p-6 pt-12 custom-scrollbar space-y-6">
                            {messages.map((m, i) => (
                                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`} style={{animation: 'fade-in-up 0.4s ease-out both'}}>
                                    
                                    {/* Bot Avatar */}
                                    {m.role === 'bot' && (
                                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center mr-3 mt-1 shadow-md">
                                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                        </div>
                                    )}

                                    <div className={`max-w-[75%] rounded-2xl px-5 py-4 shadow-sm msg-content ${m.role === 'user' ? 'bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-tr-sm' : 'bg-white border border-gray-100 text-gray-800 rounded-tl-sm shadow-[0_4px_20px_rgba(0,0,0,0.03)]'}`}>
                                        {m.role === 'user' ? <p className="text-sm font-medium text-white">{m.text}</p> : formatMessage(m.text)}
                                    </div>

                                    {/* User Avatar */}
                                    {m.role === 'user' && (
                                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center ml-3 mt-1 shadow-md border-2 border-white">
                                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                        </div>
                                    )}
                                </div>
                            ))}

                            {isTyping && (
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
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Chat Input */}
                        <div className="p-6 pb-4 z-10 flex-shrink-0 relative overflow-visible bg-transparent">
                            <form onSubmit={handleSend} className="relative flex items-center group max-w-5xl mx-auto input-glow rounded-[1.25rem] transition-shadow duration-500 z-20">
                                {/* Animated Ambient Glow Behind Input */}
                                <div className={`absolute -inset-1.5 bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 rounded-[1.5rem] blur-lg transition duration-700 opacity-20 ${input.trim() ? 'opacity-40 animate-pulse' : 'group-hover:opacity-30'}`}></div>
                                
                                <div className="relative w-full flex items-center bg-white rounded-[1.25rem] border-2 border-gray-100 group-hover:border-indigo-200 focus-within:border-indigo-400 transition-all duration-300">
                                    {/* Search Indicator Dot */}
                                    <div className="absolute left-6 flex items-center justify-center pointer-events-none">
                                        <div className="relative flex h-3.5 w-3.5">
                                          <span className={`absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75 ${input.trim() ? 'animate-ping' : ''}`}></span>
                                          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-indigo-500"></span>
                                        </div>
                                    </div>

                                    <input type="text" value={input} onChange={e => setInput(e.target.value)}
                                           placeholder="Enter target plate, timestamp, or camera node..." 
                                           className="w-full bg-transparent rounded-[1.25rem] pl-14 pr-16 py-4 text-[15px] font-bold text-gray-800 outline-none transition-all placeholder-gray-400" />
                                    
                                    <button type="submit" disabled={isTyping || !input.trim()} 
                                            className="absolute right-2.5 bg-gradient-to-r from-indigo-600 to-blue-500 text-white w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-300 transform hover:scale-110 disabled:opacity-40 disabled:hover:scale-100 shadow-[0_0_20px_rgba(79,70,229,0.4)] disabled:shadow-none overflow-hidden group/btn">
                                            <svg className={`w-5 h-5 transform transition-transform duration-300 ${input.trim() ? '-rotate-45 group-hover/btn:translate-x-1 group-hover/btn:-translate-y-1' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                                    </button>
                                </div>
                            </form>
                            
                            <p className="text-center text-[10px] font-black text-gray-400 uppercase tracking-widest mt-5 flex items-center justify-center space-x-3">
                                <span>Powered by NEXTRA AI</span>
                                <span className="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>
                                <span className="text-indigo-400 flex items-center">
                                    <svg className="w-3 h-3 mr-1 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    Deep-Search Telemetry Active
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

class ErrorBoundary extends React.Component {
    constructor(props) { super(props); this.state = { hasError: false, error: null }; }
    static getDerivedStateFromError(error) { return { hasError: true, error }; }
    render() { 
        if (this.state.hasError) return <div style={{color:'white', padding:'40px', background:'red'}}><h1>UI Crash!</h1><pre>{this.state.error.toString()}</pre></div>; 
        return this.props.children; 
    }
}




export default ChatApp;
