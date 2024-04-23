plus_textrecog_data_root = 'data/plus'        # 数据集根目录

plus_textrecog_train = dict(
    type='OCRDataset',
    data_root=plus_textrecog_data_root,     # 数据根目录
    ann_file='train.json',      # 标注文件名称
    pipeline=None)

plus_textrecog_test = dict(
    type='OCRDataset',
    data_root=plus_textrecog_data_root,
    ann_file='test.json',
    test_mode=True,
    pipeline=None)
