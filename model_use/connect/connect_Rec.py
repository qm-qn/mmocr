from mmocr.apis import TextRecInferencer
import json

model_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster_IAM_ocren2100_maxepochs192_Tmax8_etamin4e-6_lr4e-4/_base_aster_ocren2100.py'
weight_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster_IAM_ocren2100_maxepochs192_Tmax8_etamin4e-6_lr4e-4/epoch_192.pth'
# 读取模型
inferencer = TextRecInferencer(model=model_path, weights=weight_path, device='cuda:0')

input_path = '/home/yuziyang/mmocr/model_use/connect/files/noblank.jpg'
output_path = '/home/yuziyang/mmocr/model_use/connect/files/rec'
inferencer(input_path, out_dir=output_path, save_pred=True, save_vis=True)
