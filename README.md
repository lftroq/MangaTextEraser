# 🧠 TextEraserAI — Automatic Text Removal for Manga Translation 📚

[![YOLOv5](https://img.shields.io/badge/Model-YOLOv5-orange.svg)](https://github.com/ultralytics/yolov5)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google Colab](https://img.shields.io/badge/Run-Google%20Colab-yellow.svg)](https://colab.research.google.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 📖 Overview
**TextEraserAI** is an **AI-powered tool** that automatically detects and removes dialogue text from manga or comic panels, making the translation workflow faster and easier.  
Instead of relying on OCR-based text recognition, our model focuses on detecting **speech bubble text regions** directly using **YOLOv5**, improving speed and reducing training complexity.

---

## 🚀 Features
- 🖼️ **Automatic text detection and erasing** using YOLOv5.  
- ⚙️ **Batch image processing** — upload multiple pages at once.  
- 👀 **Preview and download** processed pages.  
- 🌐 **Simple web interface** for ease of use (built with HTML & CSS mockups).  
- ⚡ **Fast inference** — optimized for Google Colab GPU acceleration.  

---

## 🧩 Technical Summary
| Component | Description |
|------------|--------------|
| **Model** | YOLOv5 (custom-trained) |
| **Dataset** | Manga pages collected from open sources (e.g., Rawkuma, MangaDex) |
| **Annotation** | Automatically labeled text bubbles using custom difference-based algorithm |
| **Training Env** | Google Colab + PyTorch |
| **Input Format** | `.png` / `.jpg` images |
| **Output** | Cleaned image with erased text regions |
| **Performance** | mAP ≈ **0.87** (stable for most manga datasets) |

---

## 🧮 Workflow
1. **Data Collection:** Gather raw manga pages from official or fan-scan sources.  
2. **Pre-processing:** Remove dialogues manually in reference images → generate labels automatically.  
3. **Label Format:** YOLOv5 standard (`class x_center y_center width height`).  
4. **Model Training:** Fine-tuned on Colab using `train.py` with 640×640 image size, batch=16, epochs=100.  
5. **Testing & Evaluation:** Measured Precision, Recall, F1-score, and mAP.  
6. **Deployment:** Integrated into a web app with upload, preview, and download functions.

---

## 💻 Quick Start
```bash
# Clone repository
git clone https://github.com/<your-username>/TextEraserAI.git
cd TextEraserAI

# Install dependencies
pip install -r requirements.txt

# (Optional) Train model
python train.py --img 640 --batch 16 --epochs 100 --data data.yaml --weights yolov5s.pt

# Run detection on test images
python detect.py --weights runs/train/exp/weights/best.pt --source ./test
