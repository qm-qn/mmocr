_base_ = [
    '_base_dbnet_r18_fpnc.py',
    '../_base_/datasets/icdar2015.py',  # 导入数据集配置文件
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_sgd_1200e.py',
]

icdar2015_textdet_train = _base_.icdar2015_textdet_train            # 指定训练集
icdar2015_textdet_train.pipeline = _base_.train_pipeline   # 指定训练集使用的数据流水线
icdar2015_textdet_test = _base_.icdar2015_textdet_test              # 指定测试集
icdar2015_textdet_test.pipeline = _base_.test_pipeline     # 指定测试集使用的数据流水线

train_dataloader = dict(
    batch_size=16,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=icdar2015_textdet_train)    # 在 train_dataloader 中指定使用的训练数据集

val_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=icdar2015_textdet_test)    # 在 val_dataloader 中指定使用的验证数据集

test_dataloader = val_dataloader