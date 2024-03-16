ocren_textrecog_data_root = 'data/ocren_00/Z_ocren_01_dataset_train'        # 数据集根目录

ocren_textrecog_train = dict(
    type='OCRDataset',
    data_root=ocren_textrecog_data_root,     # 数据根目录
    ann_file='myIAM_ocren_01_train.json',      # 标注文件名称
    pipeline=None)

ocren_textrecog_test = dict(
    type='OCRDataset',
    data_root=ocren_textrecog_data_root,
    ann_file='myIAM_ocren_01_test.json',
    test_mode=True,
    pipeline=None)
