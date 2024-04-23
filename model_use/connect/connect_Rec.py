from mmocr.apis import TextRecInferencer

model_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster/TAL_ocren_IAM__93/TAL_ocren_IAM.py'
weight_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster/TAL_ocren_IAM__93/epoch_93.pth'
# 读取模型
inferencer = TextRecInferencer(model=model_path, weights=weight_path, device='cuda:0')

input_path = '/home/yuziyang/mmocr/model_use/connect/files/noblank'
output_path = '/home/yuziyang/mmocr/model_use/connect/files/rec'

inferencer(input_path, out_dir=output_path, save_pred=True, save_vis=True)
