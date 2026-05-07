from flask import Flask, render_template, request, jsonify, session
import json, os, uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "friendship-rules-secret-2026"

# In-memory storage (no database needed)
documents = {}

TEMPLATES = {
    "blank": {
        "name": "Blank",
        "color": "#ffffff",
        "accent": "#4CAF50",
        "icon": "📄",
        "content": ""
    },
    "green_pact": {
        "name": "Green Pact",
        "color": "#e8f5e9",
        "accent": "#2e7d32",
        "icon": "🤝",
        "content": """<h1 style="color:#2e7d32">Our Friendship Pact</h1>
<p><strong>Between:</strong> _______ and _______</p>
<h2>📌 Rule 1: Honesty</h2>
<p>We promise to always be honest with each other, even when it's hard.</p>
<h2>📌 Rule 2: Loyalty</h2>
<p>We stick up for each other, no matter what.</p>
<h2>📌 Rule 3: Respect</h2>
<p>We treat each other with kindness and respect at all times.</p>
<h2>📌 Rule 4: Support</h2>
<p>We are there for each other through good times and bad.</p>
<p><em>Signed on: {date}</em></p>""".replace("{date}", datetime.now().strftime("%B %d, %Y"))
    },
    "blue_bond": {
        "name": "Blue Bond",
        "color": "#e3f2fd",
        "accent": "#1565c0",
        "icon": "💙",
        "content": """<h1 style="color:#1565c0">💙 The Friendship Bond</h1>
<p>This bond is made between <strong>_______</strong> and <strong>_______</strong></p>
<hr>
<h2>Our Golden Rules:</h2>
<ul>
<li>Always listen before speaking</li>
<li>Never share secrets without permission</li>
<li>Celebrate each other's wins</li>
<li>Forgive and don't hold grudges</li>
<li>Check in when life gets tough</li>
</ul>
<h2>Our Promise:</h2>
<p>We promise to follow these rules and be the best friends we can be.</p>"""
    },
    "sunset_vibes": {
        "name": "Sunset Vibes",
        "color": "#fff3e0",
        "accent": "#e65100",
        "icon": "🌅",
        "content": """<h1 style="color:#e65100">🌅 Friends Forever Charter</h1>
<p><em>A document of love, laughter, and lasting friendship.</em></p>
<h2>Chapter 1: Communication</h2>
<p>We agree to always talk things out. No silent treatments. No ghosting. Real talk only.</p>
<h2>Chapter 2: Boundaries</h2>
<p>We respect each other's space, time, and personal limits.</p>
<h2>Chapter 3: Fun</h2>
<p>We make time to have fun together — at least once a month!</p>
<h2>Chapter 4: Conflict Resolution</h2>
<p>When we fight, we cool off, then talk calmly. No low blows allowed.</p>"""
    },
    "purple_squad": {
        "name": "Purple Squad",
        "color": "#f3e5f5",
        "accent": "#6a1b9a",
        "icon": "💜",
        "content": """<h1 style="color:#6a1b9a">💜 Squad Rules</h1>
<p><strong>Squad Name:</strong> _______</p>
<p><strong>Members:</strong> _______, _______, _______</p>
<hr>
<h2>🔒 What Stays in the Squad</h2>
<p>All personal conversations and secrets stay within the squad.</p>
<h2>🤣 Roasting Rules</h2>
<p>Friendly roasting is allowed, but we NEVER cross the line into real hurt.</p>
<h2>🆘 Emergency Clause</h2>
<p>Any squad member in need gets priority — no questions asked.</p>
<h2>🎉 Celebration Rule</h2>
<p>We celebrate every win, big or small, together.</p>"""
    },
    "minimal_clean": {
        "name": "Clean & Minimal",
        "color": "#fafafa",
        "accent": "#212121",
        "icon": "✨",
        "content": """<h1>Friendship Agreement</h1>
<p>Date: {date}</p>
<p>Parties: _______ · _______</p>
<br>
<p>1. We are kind.</p>
<p>2. We are honest.</p>
<p>3. We are present.</p>
<p>4. We forgive.</p>
<p>5. We grow together.</p>
<br>
<p><em>Simple. Real. Ours.</em></p>""".replace("{date}", datetime.now().strftime("%Y-%m-%d"))
    }
}

@app.route("/")
def index():
    return render_template("index.html", templates=TEMPLATES)

@app.route("/editor/<doc_id>")
def editor(doc_id):
    doc = documents.get(doc_id)
    if not doc:
        return "Document not found", 404
    return render_template("editor.html", doc=doc, doc_id=doc_id)

@app.route("/api/new", methods=["POST"])
def new_doc():
    data = request.json
    template_key = data.get("template", "blank")
    template = TEMPLATES.get(template_key, TEMPLATES["blank"])
    doc_id = str(uuid.uuid4())[:8]
    documents[doc_id] = {
        "id": doc_id,
        "title": data.get("title", "Untitled Friendship Rules"),
        "content": template["content"],
        "template": template_key,
        "color": template["color"],
        "accent": template["accent"],
        "created": datetime.now().strftime("%B %d, %Y"),
        "updated": datetime.now().strftime("%H:%M")
    }
    return jsonify({"doc_id": doc_id})

@app.route("/api/save/<doc_id>", methods=["POST"])
def save_doc(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    documents[doc_id]["content"] = data.get("content", "")
    documents[doc_id]["title"] = data.get("title", documents[doc_id]["title"])
    documents[doc_id]["updated"] = datetime.now().strftime("%H:%M")
    return jsonify({"status": "saved", "time": documents[doc_id]["updated"]})

@app.route("/api/docs")
def list_docs():
    return jsonify(list(documents.values()))

@app.route("/api/delete/<doc_id>", methods=["DELETE"])
def delete_doc(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Not found"}), 404
    del documents[doc_id]
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))