cocotextv2_textdet_data_root = 'data/cocotextv2'        # 数据集根目录

cocotextv2_textdet_train = dict(
    type='OCRDataset',
    data_root=cocotextv2_textdet_data_root,     # 数据根目录
    ann_file='textdet_train.json',      # 标注文件名称
    filter_cfg=dict(filter_empty_gt=True, min_size=32),     # 数据过滤
    pipeline=None)

cocotextv2_textdet_val = dict(
    type='OCRDataset',
    data_root=cocotextv2_textdet_data_root,
    ann_file='textdet_val.json',
    test_mode=True,
    pipeline=None)
