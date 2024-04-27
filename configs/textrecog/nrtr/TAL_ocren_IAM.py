_base_ = [
    '../_base_/datasets/IAM.py',
    '../_base_/datasets/ocren.py',
    '../_base_/datasets/TAL.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_adam_base.py',
    '_base_nrtr_resnet31.py',
]

# optimizer settings
train_cfg = dict(max_epochs=6)
# learning policy
param_scheduler = [
    dict(type='MultiStepLR', milestones=[3, 4], end=6),
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

train_dataset = dict(
    type='ConcatDataset', datasets=train_list, pipeline=_base_.train_pipeline)
test_dataset = dict(
    type='ConcatDataset', datasets=test_list, pipeline=_base_.test_pipeline)

train_dataloader = dict(
    batch_size=384,
    num_workers=24,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=train_dataset)

test_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=test_dataset)

val_dataloader = test_dataloader

val_evaluator = dict(
    dataset_prefixes=['TAL', 'IAM', 'ocren'])
test_evaluator = val_evaluator

auto_scale_lr = dict(base_batch_size=384)
