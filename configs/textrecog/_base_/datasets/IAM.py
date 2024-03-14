IAM_textrecog_data_root = 'data/IAM/words_original'        # 数据集根目录

IAM_textrecog_train = dict(
    type='OCRDataset',
    data_root=IAM_textrecog_data_root,     # 数据根目录
    ann_file='words_train.json',      # 标注文件名称
    pipeline=None)

IAM_textrecog_test = dict(
    type='OCRDataset',
    data_root=IAM_textrecog_data_root,
    ann_file='words_test.json',
    test_mode=True,
    pipeline=None)
