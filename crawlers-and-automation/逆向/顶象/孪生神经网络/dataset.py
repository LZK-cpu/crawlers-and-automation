from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T

class PairDataset(Dataset):
    def __init__(self, pair_file):
        self.pairs = []
        with open(pair_file,'r',encoding='utf-8') as f:
            for line in f:
                a, b, y = line.strip().split()
                self.pairs.append((a, b, int(y)))

        self.transform = T.Compose([
            T.Resize((100, 100)),
            T.RandomHorizontalFlip(),
            T.ColorJitter(0.2, 0.2, 0.2),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
        ])

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        a, b, y = self.pairs[idx]
        img1 = self.transform(Image.open(a).convert("RGB"))
        img2 = self.transform(Image.open(b).convert("RGB"))
        return img1, img2, y
