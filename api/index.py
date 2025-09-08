from flask import Flask, request, render_template, jsonify
from ocr_core import run_ocr
import tempfile
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" in request.files:
            img_file = request.files["image"]
            temp_path = tempfile.mktemp(suffix=".png")
            img_file.save(temp_path)
            result = run_ocr(temp_path)
            os.remove(temp_path)
            return jsonify({"text": result})
    return render_template("index.html")

# Vercelがこの関数を呼び出す
def handler(event, context):
    return app(event, context)