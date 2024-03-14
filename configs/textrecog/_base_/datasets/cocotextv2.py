cocotextv2_textrecog_data_root = 'data/cocotextv2'

cocotextv2_textrecog_train = dict(
    type='OCRDataset',
    data_root=cocotextv2_textrecog_data_root,
    ann_file='textrecog_train.json',
    pipeline=None)

cocotextv2_textrecog_test = dict(
    type='OCRDataset',
    data_root=cocotextv2_textrecog_data_root,
    ann_file='textrecog_test.json',
    test_mode=True,
    pipeline=None)
