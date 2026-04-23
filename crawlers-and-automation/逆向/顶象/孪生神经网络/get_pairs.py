import os
import random

dataset_dir = "chinese_image"
output_file = "pairs.txt"

NEG_PER_ANCHOR = 5
POS_LIMIT = 5

pairs = set()

classes = [
    c for c in os.listdir(dataset_dir)
    if os.path.isdir(os.path.join(dataset_dir, c))
]

print("类别数:", len(classes))

class_imgs = {}

for cls in classes:
    cls_path = os.path.join(dataset_dir, cls)

    imgs = [
        os.path.join(cls_path, f).replace("\\", "/")
        for f in os.listdir(cls_path)
        if os.path.isfile(os.path.join(cls_path, f))
    ]

    if len(imgs) > 0:
        class_imgs[cls] = imgs

for cls, imgs in class_imgs.items():

    if len(imgs) < 1:
        continue

    other_classes = [c for c in classes if c != cls]

    for anchor in imgs:
        pairs.add((anchor, anchor, 1))
        pos_pool = [i for i in imgs if i != anchor]

        if len(pos_pool) > 0:
            pos_samples = random.sample(
                pos_pool,
                min(POS_LIMIT, len(pos_pool))
            )

            for img in pos_samples:
                pairs.add((anchor, img, 1))
        for _ in range(NEG_PER_ANCHOR):
            neg_cls = random.choice(other_classes)
            neg_imgs = class_imgs.get(neg_cls, [])

            if len(neg_imgs) == 0:
                continue

            neg_img = random.choice(neg_imgs)
            pairs.add((anchor, neg_img, 0))

pairs = list(pairs)
random.shuffle(pairs)

with open(output_file, "w", encoding="utf-8") as f:
    for a, b, label in pairs:
        f.write(f"{a} {b} {label}\n")

print("pairs数量:", len(pairs))
print("保存路径:", output_file)