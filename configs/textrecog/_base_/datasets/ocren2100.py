ocren2100_textrecog_data_root = 'data/ocren2100/img'        # 数据集根目录

ocren2100_textrecog_train = dict(
    type='OCRDataset',
    data_root=ocren2100_textrecog_data_root,     # 数据根目录
    ann_file='../train.json',      # 标注文件名称
    pipeline=None)

ocren2100_textrecog_test = dict(
    type='OCRDataset',
    data_root=ocren2100_textrecog_data_root,
    ann_file='../test.json',
    test_mode=True,
    pipeline=None)
