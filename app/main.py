from flask import Flask, render_template, request, abort
import os

print("Templates Directory:", os.path.join(os.getcwd(), 'templates'))


app = Flask(__name__)

FILE_DB = {
    "1": ("Project Overview", "files/1_project_overview.txt"),
    "2": ("Product Roadmap", "files/2_roadmap.txt"),
    "3": ("Budget Summary", "files/3_budget_summary.txt"),
    "4": ("Internal Notes", "files/4_internal_notes.txt"),
    "5": ("Operation Whispergrid Memo", "files/5_whispergrid_memo.txt")
}

VISIBLE_FILES = ["1", "2", "3"]

@app.route("/")
def index():
    files = [(fid, FILE_DB[fid][0]) for fid in VISIBLE_FILES]
    return render_template("index.html", files=files)

@app.route("/file")
def get_file():
    file_id = request.args.get("id")
    file_entry = FILE_DB.get(file_id)

    if not file_entry:
        abort(404, "File not found.")

    title, path = file_entry
    try:
        with open(path, "r") as f:
            content = f.read()
        return render_template("index.html", files=[(fid, FILE_DB[fid][0]) for fid in VISIBLE_FILES],
                               selected_id=file_id, file_content=content, file_title=title)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

