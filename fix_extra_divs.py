import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the extra divs before LIVE AI PREVIEW MODAL
bad_spot = """                </div>
            </div>

                </div>
                </div>
            </div>

            {/* LIVE AI PREVIEW MODAL */}"""

good_spot = """                </div>
            </div>
        </div>

            {/* LIVE AI PREVIEW MODAL */}"""

content = content.replace(bad_spot, good_spot)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed extra divs!")
