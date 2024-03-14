# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW',
        lr=1e-4,
        betas=(0.9, 0.999),
        eps=1e-08,
        weight_decay=0.05))
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=96, val_interval=1)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

# learning policy
param_scheduler = [
    dict(
        type='CosineAnnealingLR',
        T_max=8,
        eta_min=8e-4,
        convert_to_iter_based=True)
]
