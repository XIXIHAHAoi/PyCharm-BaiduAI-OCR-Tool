from aip import AipOcr
import os
from docx import Document

# ===================== 【配置区】替换为你的百度密钥 =====================
APP_ID = "你的APP_ID"
API_KEY = "你的API_KEY"
SECRET_KEY = "你的SECRET_KEY"
# =====================================================================

# 初始化百度OCR客户端
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 项目路径配置（PyCharm自动识别，无需修改）
IMAGE_DIR = "images"  # 图片存放文件夹
OUTPUT_DIR = "output"  # 结果导出文件夹

def init_dir():
    """初始化文件夹，不存在则自动创建"""
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

def get_image_data(file_path):
    """读取图片二进制数据"""
    with open(file_path, "rb") as f:
        return f.read()

def recognize_text(image_path):
    """调用百度API进行高精度文字识别"""
    try:
        image = get_image_data(image_path)
        # 高精度识别（识别率远高于普通模式）
        result = client.basicAccurate(image)
        # 提取识别结果
        words_list = [item["words"] for item in result.get("words_result", [])]
        return "\n".join(words_list)
    except Exception as e:
        return f"识别失败：{str(e)}"

def save_to_file(content, filename):
    """同时导出TXT和Word文档"""
    # 导出TXT
    txt_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 导出Word
    docx_path = os.path.join(OUTPUT_DIR, f"{filename}.docx")
    doc = Document()
    doc.add_paragraph(content)
    doc.save(docx_path)

def batch_ocr():
    """批量识别images文件夹内所有图片"""
    init_dir()
    print("=" * 50)
    print("📸 开始批量识别图片文字...")
    print("=" * 50)

    # 遍历图片文件
    image_suffix = [".jpg", ".png", ".jpeg", ".bmp"]
    all_result = ""

    for file in os.listdir(IMAGE_DIR):
        file_path = os.path.join(IMAGE_DIR, file)
        # 判断是否为图片
        if os.path.isfile(file_path) and any(file.endswith(suf) for suf in image_suffix):
            print(f"正在识别：{file}")
            text = recognize_text(file_path)
            all_result += f"===== {file} 识别结果 =====\n{text}\n\n"

    # 保存总结果
    if all_result:
        save_to_file(all_result, "识别结果汇总")
        print("=" * 50)
        print("✅ 识别完成！结果已保存到 output 文件夹")
        print("=" * 50)
    else:
        print("❌ 未找到可识别的图片，请将图片放入 images 文件夹")

# ===================== 主程序：一键运行 =====================
if __name__ == "__main__":
    batch_ocr()