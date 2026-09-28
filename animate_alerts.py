import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add showSidebar state
if "const [showSidebar, setShowSidebar] = React.useState(true);" not in content:
    content = content.replace(
        "const [loading, setLoading] = React.useState(true);",
        "const [loading, setLoading] = React.useState(true);\n    const [showSidebar, setShowSidebar] = React.useState(true);"
    )

# 2. Add Hamburger Button to Navbar
if "setShowSidebar" not in content.split('className="text-2xl font-black')[0]:
    hamburger = '<button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50 mr-4"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg></button>'
    content = content.replace(
        '<h1 className="text-2xl font-black',
        hamburger + '\n                        <h1 className="text-2xl font-black'
    )

# 3. Animate Left Panel Width
old_left = '<div className="w-full lg:w-2/3 h-full flex flex-col bg-white/90 backdrop-blur-3xl rounded-[22px] border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] overflow-hidden">'
new_left = '<div className={`h-full flex flex-col bg-white/90 backdrop-blur-3xl rounded-[22px] border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? "w-full lg:w-2/3" : "w-full"}`}>'
content = content.replace(old_left, new_left)

# 4. Animate Right Panel Width
old_right = '<div className="hidden lg:flex w-1/3 h-full flex-col">'
new_right = '<div className={`h-full flex-col transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] overflow-hidden ${showSidebar ? "w-1/3 opacity-100 flex" : "w-0 opacity-0 hidden"}`}>'
content = content.replace(old_right, new_right)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated alerts.html")
