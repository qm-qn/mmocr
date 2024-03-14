from mmocr.apis import MMOCRInferencer
# 读取模型
ocr = MMOCRInferencer(rec='/home/yuziyang/mmocr/work_dirs/rec/lines/aster_IAM/maxepochs24_Tmax6_etamin4e-6_lr4e-4/_base_aster_IAM.py', rec_weights='/home/yuziyang/mmocr/work_dirs/rec/lines/aster_IAM/maxepochs24_Tmax6_etamin4e-6_lr4e-4/epoch_24.pth', device='cuda:0')
# 进行推理并可视化结果
ocr('ocrencut/10126030/', out_dir='m_outputs/0301/MMOCR/1612', save_pred=True, save_vis=True)