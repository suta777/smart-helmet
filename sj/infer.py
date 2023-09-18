from transformers import pipeline
import torch
import os

def infer(video_cls,video_path= "new_sample.mp4"):
    print(video_path)
    pre = (video_cls(video_path))
    pre_arr = []
    for p in pre:
        pre_arr.append(p['score'])

    pre_arr = torch.tensor(pre_arr)
    class_idx = pre_arr.argmax(-1).item()

    if class_idx == 0:
        label = "accident"
    else:
        label = "driving"
    print(label)
    return label

    #infer(video_cls=pipeline(model="lake-crimsonn/acc-dri-videomae-base"),video_patqh=os.path.join('videos_in', 'temp4.mp4'))