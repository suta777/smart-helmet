import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image

def draw_melspectogram(audiofile):
    # 오디오 불러오기
    y, sr = librosa.load(audiofile)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512)
    mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

    # 이미지 그리기
    fig, ax = plt.subplots(figsize=(5, 4))
    librosa.display.specshow(mel_spec, sr=sr, hop_length=512, x_axis='time', y_axis='log', ax=ax)
    ax.axis('off')
    # plt.show()

    # 이미지 저장하기
    savefile = audiofile[:-4] + '.jpg'
    plt.savefig(savefile, bbox_inches='tight', pad_inches=0)
    plt.close()

    return savefile

model = torch.load('models/audio.pth',map_location=torch.device('cpu'))

def audio_predict(audiofile, model):
    file_path = draw_melspectogram(audiofile)
    image = Image.open(file_path)

    test_transforms = transforms.Compose(
        [
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406),std=(0.229,0.224,0.225))
        ]
    )
    image = test_transforms(image).unsqueeze(0).to('cpu')
    model.to('cpu')

    with torch.no_grad():
        outputs = model(image)
        _, pred = torch.max(outputs.data,1)

    return not pred.item()


