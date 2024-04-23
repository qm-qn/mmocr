# training schedule for 1x
_base_ = [
    '_base_crnn_mini-vgg.py',
    '../_base_/datasets/IAM.py',
    '../_base_/datasets/ocren.py',
    '../_base_/datasets/TAL.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_adadelta_5e.py',
]

# dataset settings
train_list = [
    _base_.TAL_textrecog_train,
    _base_.IAM_textrecog_train,
    _base_.ocren_textrecog_train
]
test_list = [
    _base_.TAL_textrecog_test,
    _base_.IAM_textrecog_test,
    _base_.ocren_textrecog_test,
]

default_hooks = dict(logger=dict(type='LoggerHook', interval=100))

train_dataloader = dict(
    batch_size=1024,
    num_workers=24,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='ConcatDataset',
        datasets=train_list,
        pipeline=_base_.train_pipeline))
test_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='ConcatDataset',
        datasets=test_list,
        pipeline=_base_.test_pipeline))
val_dataloader = test_dataloader

val_evaluator = dict(
    dataset_prefixes=['TAL', 'IAM', 'ocren'])
test_evaluator = val_evaluator

auto_scale_lr = dict(base_batch_size=64 * 4)

load_from = '/public/yuziyang/work_dirs/rec/new_dict/lines/crnn/TAL_ocren_IAM_maxepochs96_Tmax8_etamin4e-06_lr2e-04/epoch_33.pth'
