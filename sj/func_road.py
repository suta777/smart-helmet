from PIL import Image
import torch
from torchvision import transforms
import time
import cv2
import os
device = 'cuda'
model = torch.load(os.path.join('models', 'road_model.pt'), map_location=device)
model.eval()

transform_test = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

name = ['sidewalk','driveway']

async def road(image):
    y, x = image.shape[0], image.shape[1]
    #cv2.rectangle(image, (2 * x // 7, y // 3), (5 * x // 7, y), (0, 0, 255, 255), 2)
    image = Image.fromarray(image)
    image = image.crop((2 * x // 7, y // 3, 5 * x // 7, y))
    image = image.convert('RGB')
    image = transform_test(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        #print(name[preds[0].int()])
        return name[preds[0].int()]  # 결과 반환