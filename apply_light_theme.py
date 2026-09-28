import glob

replacements = {
    # Backgrounds
    'bg-slate-950': 'bg-gray-100',
    'bg-[#0F172A]': 'bg-gray-100',
    'bg-slate-900': 'bg-gray-50',
    'bg-slate-800': 'bg-white',
    'bg-[#1E293B]': 'bg-white',
    'bg-slate-700': 'bg-gray-100',
    'bg-slate-600': 'bg-gray-200',
    
    # Borders
    'border-slate-800': 'border-gray-200',
    'border-slate-700': 'border-gray-200',
    'border-slate-600': 'border-gray-300',
    'border-slate-500': 'border-gray-300',
    'border-slate-700/50': 'border-gray-200',
    
    # Text
    'text-white': 'text-gray-900',
    'text-slate-100': 'text-gray-900',
    'text-slate-200': 'text-gray-800',
    'text-slate-300': 'text-gray-700',
    'text-slate-400': 'text-gray-600',
    'text-slate-500': 'text-gray-500',
    
    # Hovers
    'hover:bg-slate-700': 'hover:bg-gray-100',
    'hover:bg-slate-800': 'hover:bg-gray-200',
    'hover:text-white': 'hover:text-gray-900',
    
    # Accents (Cyan -> Indigo/Blue)
    'text-cyan-400': 'text-indigo-600',
    'text-cyan-500': 'text-indigo-600',
    'bg-cyan-600': 'bg-indigo-600',
    'bg-cyan-500': 'bg-indigo-500',
    'hover:bg-cyan-500': 'hover:bg-indigo-700',
    'border-cyan-500': 'border-indigo-500',
    'ring-cyan-500': 'ring-indigo-500',
    'bg-cyan-500/10': 'bg-indigo-500/10',
    'bg-cyan-500/20': 'bg-indigo-500/20',
    
    # Shadows
    'shadow-[0_0_15px_rgba(34,211,238,0.3)]': 'shadow-lg shadow-indigo-500/20',
    'shadow-[0_0_10px_rgba(34,211,238,0.5)]': 'shadow-md shadow-indigo-500/20',
    'shadow-[0_0_10px_rgba(34,211,238,0.2)]': 'shadow-sm',
    'shadow-[0_0_10px_rgba(34,211,238,0.3)]': 'shadow-sm',
    
    # Specific UI Elements
    'text-green-400': 'text-emerald-600',
    'text-rose-400': 'text-rose-600',
    'bg-slate-900/50': 'bg-white/80',
    'bg-slate-800/80': 'bg-white/90',
    'bg-slate-800/50': 'bg-white/50',
    "radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)": "radial-gradient(circle at center, #f9fafb 0%, #f3f4f6 100%)",
    'bg-gradient-to-t from-[#0F172A] via-[#0F172A] to-transparent': 'bg-gradient-to-t from-gray-100 via-gray-100 to-transparent',
    '.msg-text strong { color: #fff;': '.msg-text strong { color: #111827;',
    'rgba(34, 211, 238, 0.1)': 'rgba(79, 70, 229, 0.1)',
    'rgba(255, 255, 255, 0.1)': 'rgba(0, 0, 0, 0.1)',
    "color: '#94a3b8'": "color: '#4b5563'",
    "color: '#fff'": "color: '#111827'",
    "backgroundColor: 'rgba(34, 211, 238, 0.2)'": "backgroundColor: 'rgba(79, 70, 229, 0.2)'",
    "borderColor: '#22d3ee'": "borderColor: '#4f46e5'",
}

post_corrections = {
    # Fix inverted buttons
    'bg-indigo-600 text-gray-900': 'bg-indigo-600 text-white',
    'bg-indigo-500 text-gray-900': 'bg-indigo-500 text-white',
    'bg-rose-500 text-gray-900': 'bg-rose-500 text-white',
    'bg-emerald-600 text-gray-900': 'bg-emerald-600 text-white',
    
    # Fix nav active state
    'bg-indigo-600 text-gray-900 shadow': 'bg-indigo-600 text-white shadow-md ring-2 ring-indigo-300',
    'bg-indigo-600 text-white shadow': 'bg-indigo-600 text-white shadow-md ring-2 ring-indigo-300',
    
    # Fix avatars
    'text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"': 'text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"',
}

# Mobile responsiveness patches
responsive_patches = {
    'className="flex space-x-1 border border-gray-200 rounded-lg p-1 bg-white"': 'className="flex flex-wrap gap-1 border border-gray-200 rounded-lg p-1 bg-white md:space-x-1"',
    'className="max-w-5xl mx-auto bg-white rounded-xl shadow-2xl overflow-hidden border border-gray-200"': 'className="w-full max-w-5xl mx-auto bg-white rounded-xl shadow-xl overflow-x-auto border border-gray-200 sm:px-6 lg:px-8"',
    'className="flex items-center space-x-4"': 'className="flex items-center space-x-2 md:space-x-4"',
}

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    for old, new in post_corrections.items():
        content = content.replace(old, new)
        
    for old, new in responsive_patches.items():
        content = content.replace(old, new)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Light Theme successfully applied across all files!")
