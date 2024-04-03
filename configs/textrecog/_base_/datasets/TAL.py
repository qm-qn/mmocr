TAL_textrecog_data_root = 'data/TAL'        # 数据集根目录

TAL_textrecog_train = dict(
    type='OCRDataset',
    data_root=TAL_textrecog_data_root,     # 数据根目录
    ann_file='train.json',      # 标注文件名称
    pipeline=None)

TAL_textrecog_test = dict(
    type='OCRDataset',
    data_root=TAL_textrecog_data_root,
    ann_file='test.json',
    test_mode=True,
    pipeline=None)
