import glob

replacements = {
    # Responsiveness patches (reverse first while classes are still light)
    'className="flex flex-wrap gap-1 border border-gray-200 rounded-lg p-1 bg-white md:space-x-1"': 'className="flex space-x-1 border border-slate-700 rounded-lg p-1 bg-slate-800"',
    'className="w-full max-w-5xl mx-auto bg-white rounded-xl shadow-xl overflow-x-auto border border-gray-200 sm:px-6 lg:px-8"': 'className="max-w-5xl mx-auto bg-slate-800 rounded-xl shadow-2xl overflow-hidden border border-slate-700"',
    'className="flex items-center space-x-2 md:space-x-4"': 'className="flex items-center space-x-4"',

    # Backgrounds
    'bg-gray-100': 'bg-slate-950',
    'bg-gray-50': 'bg-slate-900',
    'bg-white': 'bg-slate-800',
    'bg-gray-200': 'bg-slate-600',
    
    # Borders
    'border-gray-200': 'border-slate-700',
    'border-gray-300': 'border-slate-600',
    
    # Text
    'text-gray-900': 'text-white',
    'text-gray-800': 'text-slate-200',
    'text-gray-700': 'text-slate-300',
    'text-gray-600': 'text-slate-400',
    'text-gray-500': 'text-slate-500',
    
    # Hovers
    'hover:bg-gray-100': 'hover:bg-slate-700',
    'hover:bg-gray-200': 'hover:bg-slate-800',
    'hover:text-gray-900': 'hover:text-white',
    
    # Accents (Indigo -> Cyan)
    'text-indigo-600': 'text-cyan-400',
    'text-indigo-700': 'text-cyan-400',
    'bg-indigo-600': 'bg-cyan-600',
    'bg-indigo-500': 'bg-cyan-500',
    'hover:bg-indigo-700': 'hover:bg-cyan-500',
    'border-indigo-500': 'border-cyan-500',
    'ring-indigo-500': 'ring-cyan-500',
    'bg-indigo-500/10': 'bg-cyan-500/10',
    'bg-indigo-500/20': 'bg-cyan-500/20',
    'bg-indigo-600 text-white shadow-md ring-2 ring-indigo-300': 'bg-indigo-600 text-white shadow', # will be converted to cyan next
    
    # Shadows
    'shadow-lg shadow-indigo-500/20': 'shadow-[0_0_15px_rgba(34,211,238,0.3)]',
    'shadow-md shadow-indigo-500/20': 'shadow-[0_0_10px_rgba(34,211,238,0.5)]',
    
    # Specific UI Elements
    'text-emerald-600': 'text-green-400',
    'text-rose-600': 'text-rose-400',
    'bg-white/80': 'bg-slate-900/50',
    'bg-white/90': 'bg-slate-800/80',
    'bg-white/50': 'bg-slate-800/50',
    "radial-gradient(circle at center, #f9fafb 0%, #f3f4f6 100%)": "radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)",
    'bg-gradient-to-t from-gray-100 via-gray-100 to-transparent': 'bg-gradient-to-t from-[#0F172A] via-[#0F172A] to-transparent',
    '.msg-text strong { color: #111827;': '.msg-text strong { color: #fff;',
    'rgba(79, 70, 229, 0.1)': 'rgba(34, 211, 238, 0.1)',
    'rgba(0, 0, 0, 0.1)': 'rgba(255, 255, 255, 0.1)',
    "color: '#4b5563'": "color: '#94a3b8'",
    "color: '#111827'": "color: '#fff'",
    "backgroundColor: 'rgba(79, 70, 229, 0.2)'": "backgroundColor: 'rgba(34, 211, 238, 0.2)'",
    "borderColor: '#4f46e5'": "borderColor: '#22d3ee'",
}

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # Post corrections for indigo -> cyan
    content = content.replace('bg-indigo-600', 'bg-indigo-600') # Actually I want to keep the active button indigo, so I will replace cyan-600 to indigo-600 back?
    # Wait, in the dark theme I had bg-indigo-600 for the active tab!
    # If I mapped it to bg-cyan-600 above, let's fix it.
    content = content.replace('bg-cyan-600 text-white shadow', 'bg-indigo-600 text-white shadow')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dark Theme successfully reverted!")
