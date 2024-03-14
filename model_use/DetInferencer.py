from mmocr.apis import TextDetInferencer
# 读取模型
inferencer = TextDetInferencer(model='configs/textdet/dbnet/dbnet_r18.py', weights='work_dirs/cocotextv2/epoch_1200.pth', device='cuda:0')
# 推理
inferencer('ocren_01/10126030/', out_dir='m_outputs/0221/Det/dbnet_r18', save_pred=True, save_vis=True)