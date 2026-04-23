import torch.nn as nn


class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin

    def forward(self, e1, e2, y):
        dist = torch.norm(e1 - e2, dim=1)
        loss = y * dist**2 + (1 - y) * torch.clamp(self.margin - dist, min=0)**2
        return loss.mean()



import torch
from torch.utils.data import DataLoader
from model import SiameseNet
from dataset import PairDataset
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"

dataset = PairDataset("pairs.txt")
loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = SiameseNet().to(device)
criterion = ContrastiveLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(40):
    print("epoch", epoch)
    total_loss = 0
    pbar = tqdm(loader, desc=f"Epoch {epoch}", ncols=100)
    for x1, x2, y in pbar:
        x1, x2 = x1.to(device), x2.to(device)
        y = y.float().to(device)
        e1, e2 = model(x1, x2)
        loss = criterion(e1, e2, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch}: loss={total_loss/len(loader):.4f}")

torch.save(model.state_dict(), "model/图标点选_siamese.pth")
