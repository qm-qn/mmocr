TAL_OCR_ENG_textrecog_data_root = 'data/TAL_OCR_ENG/img'        # 数据集根目录

TAL_OCR_ENG_textrecog_train = dict(
    type='OCRDataset',
    data_root=TAL_OCR_ENG_textrecog_data_root,     # 数据根目录
    ann_file='../train.json',      # 标注文件名称
    pipeline=None)

TAL_OCR_ENG_textrecog_test = dict(
    type='OCRDataset',
    data_root=TAL_OCR_ENG_textrecog_data_root,
    ann_file='../test.json',
    test_mode=True,
    pipeline=None)
