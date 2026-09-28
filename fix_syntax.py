import glob
import re

new_voice_nav = """
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
                            className={`p-2 rounded-full border transition-all ${isActive ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-[0_0_10px_rgba(34,211,238,0.2)]' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700'}`}>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                    </button>
                    {isActive && (
                        <span className={`text-[10px] font-bold uppercase tracking-widest ${isProcessing ? 'text-rose-500 animate-pulse' : 'text-cyan-500 animate-pulse'}`}>
                            {isProcessing ? 'Command Received' : 'Listening...'}
                        </span>
                    )}
                </div>
            );
        };
"""

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace from "const VoiceNav" all the way down to the first "function" declaration
    # using re.DOTALL so it grabs all the corrupted dangling bits
    pattern = re.compile(r'const VoiceNav = .*?(?=function [A-Z])', re.DOTALL)
    
    # We substitute it with our clean new_voice_nav
    content = pattern.sub(new_voice_nav, content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Syntax error fixed in all HTML files.")
