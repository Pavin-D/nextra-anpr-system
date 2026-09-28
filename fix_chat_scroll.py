import re

with open("chat.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace scrollIntoView with safe container-only scrollTop manipulation
old_scroll = "messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });"
new_scroll = """if (messagesEndRef.current && messagesEndRef.current.parentElement) {
            messagesEndRef.current.parentElement.scrollTo({
                top: messagesEndRef.current.parentElement.scrollHeight,
                behavior: 'smooth'
            });
        }"""

content = content.replace(old_scroll, new_scroll)

with open("chat.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced scrollIntoView with precise container scrolling!")
