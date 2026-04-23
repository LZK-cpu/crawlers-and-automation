import os
import random
import shutil

# ----------------------------
# 配置
# ----------------------------
image_dir = "answerImage"    # 原始图片
label_dir = "labels"    # YOLO txt 标签
output_dir = "dataset"  # 输出目录
train_ratio = 0.8
random.seed(42)

# ----------------------------
# 创建输出目录
# ----------------------------
for split in ["train", "val"]:
    os.makedirs(os.path.join(output_dir, "images", split), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels", split), exist_ok=True)

# ----------------------------
# 获取所有图片
# ----------------------------
img_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
random.shuffle(img_files)

num_train = int(len(img_files) * train_ratio)
train_files = img_files[:num_train]
val_files = img_files[num_train:]

# ----------------------------
# 拷贝图片和标签
# ----------------------------
def copy_files(file_list, split):
    for img_file in file_list:
        base_name = os.path.splitext(img_file)[0]
        # 图片
        src_img = os.path.join(image_dir, img_file)
        dst_img = os.path.join(output_dir, "images", split, img_file)
        shutil.copy(src_img, dst_img)
        # 标签
        txt_file = base_name + ".txt"
        src_txt = os.path.join(label_dir, txt_file)
        dst_txt = os.path.join(output_dir, "labels", split, txt_file)
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt)
        else:
            print(f"Warning: 标签 {txt_file} 未找到!")

copy_files(train_files, "train")
copy_files(val_files, "val")

# ----------------------------
# 生成 data.yaml
# ----------------------------
data_yaml = f"""
train: {os.path.join(output_dir, 'images', 'train')}
val: {os.path.join(output_dir, 'images', 'val')}

nc: 1
names: ['char']
"""

yaml_path = os.path.join(output_dir, "data.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    f.write(data_yaml.strip())

print("划分完成！")
print(f"训练集: {len(train_files)} 张, 验证集: {len(val_files)} 张")
print(f"data.yaml 已生成: {yaml_path}")