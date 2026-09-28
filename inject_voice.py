import os
import glob
import re

voice_nav_code = """
        const VoiceNav = () => {
            const [isListening, setIsListening] = React.useState(false);

            const startListening = () => {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Voice Navigation is not supported in this browser.");
                    return;
                }

                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onstart = () => setIsListening(true);
                recognition.onerror = (e) => setIsListening(false);
                recognition.onend = () => setIsListening(false);

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript.toLowerCase();
                    if (transcript.includes("dashboard") || transcript.includes("overview")) window.location.href = "/";
                    else if (transcript.includes("tracking")) window.location.href = "/tracking";
                    else if (transcript.includes("blacklist")) window.location.href = "/blacklist";
                    else if (transcript.includes("geofence")) window.location.href = "/geofence";
                    else if (transcript.includes("chat") || transcript.includes("search")) window.location.href = "/chat";
                };

                recognition.start();
            };

            return (
                <button onClick={startListening} title="Voice Navigation (e.g., 'Go to Tracking')" 
                        className={`p-2 rounded-full border transition-all ${isListening ? 'bg-rose-500/20 border-rose-500 text-rose-500 animate-pulse shadow-[0_0_10px_rgba(244,63,94,0.5)]' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700'}`}>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                </button>
            );
        };
"""

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if already injected to avoid duplication
    if "const VoiceNav" in content:
        continue
        
    # 1. Inject the VoiceNav component right after <script type="text/babel">
    content = content.replace('<script type="text/babel">', '<script type="text/babel">\n' + voice_nav_code)
    
    # 2. Inject <VoiceNav /> next to the NEXTRA header
    header_pattern = r'(<h1.*?NEXTRA.*?</h1>)'
    content = re.sub(header_pattern, r'\1\n                            <VoiceNav />', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Voice Navigation successfully injected into all pages!")
