import os
import json

# 配置路径
json_dir = r"C:\Users\Administrator\Desktop\标注\GS_login"  # 你的 JSON 文件夹
label_dir = "labels"       # 输出 YOLO 标签的文件夹
os.makedirs(label_dir, exist_ok=True)

# 遍历所有 JSON 文件
for json_file in os.listdir(json_dir):
    if not json_file.endswith(".json"):
        continue

    json_path = os.path.join(json_dir, json_file)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_w = data["imageWidth"]
    image_h = data["imageHeight"]

    yolo_lines = []
    for shape in data["shapes"]:
        if shape["label"] != "char":
            continue

        # LabelMe 的矩形框点
        (x1, y1), (x2, y2) = shape["points"]
        # YOLO 坐标归一化
        x_center = ((x1 + x2) / 2) / image_w
        y_center = ((y1 + y2) / 2) / image_h
        w = (x2 - x1) / image_w
        h = (y2 - y1) / image_h

        class_id = 0  # char 类别
        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    # 输出 TXT 文件，文件名和图片名对应
    txt_file = os.path.splitext(json_file)[0] + ".txt"
    txt_path = os.path.join(label_dir, txt_file)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yolo_lines))

print("全部 JSON 转换完成！")