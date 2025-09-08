import gradio as gr
from ocr_core import run_ocr
import tempfile

def ocr_interface(image):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)
        result = run_ocr(tmp.name)
    return result

gr.Interface(
    fn=ocr_interface,
    inputs=gr.Image(type="pil", label="画像をアップロード"),
    outputs=gr.Textbox(label="OCR結果"),
    title="Yomitoku OCR Web",
    description="画像をアップロードすると、yomitokuで文字認識します。"
).launch()