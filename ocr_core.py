# ocr_core.py
import cv2
import numpy as np
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

analyzer = DocumentAnalyzer(
    configs={
        "ocr": {
            "text_detector": {"path_cfg": None},
            "text_recognizer": {"path_cfg": None},
        },
        "layout_analyzer": {
            "layout_parser": {"path_cfg": None},
            "table_structure_recognizer": {"path_cfg": None},
        },
    },
    visualize=False,
    device="cpu",  # 必要に応じて "cpu" に変更
    ignore_meta=False,
    reading_order="auto"
)

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise RuntimeError(f"画像読み込み失敗: {img_path}")
    target_min_width = 1200
    h, w = img.shape[:2]
    if w < target_min_width:
        scale = max(1.0, target_min_width / w)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    return enhanced_rgb

def extract_contents_only(ocr_json):
    all_texts = []
    for figure in ocr_json.get("figures", []):
        for para in figure.get("paragraphs", []):
            content = para.get("contents", "")
            if content:
                all_texts.append(content.strip())
    return "\n\n".join(all_texts)

def run_ocr(img_path):
    try:
        try:
            img = preprocess_image(img_path)
        except Exception:
            img = load_image(img_path)
        if isinstance(img, list):
            img = img[0]
        if not isinstance(img, np.ndarray) or not hasattr(img, "shape"):
            raise ValueError("画像形式が不正です")
        results, _, _ = analyzer(img)
        return extract_contents_only(results.dict())
    except Exception as e:
        return f"OCR処理失敗: {e}"