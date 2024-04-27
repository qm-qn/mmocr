import os
# from configs.textrecog._base_.schedules.plus_schedule_adamw_cos_6e import optim_wrapper, param_scheduler, train_cfg


def train():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    model = 'nrtr'
    name = 'TAL_ocren_IAM'
    # lr = optim_wrapper['optimizer']['lr']
    # lr = "{:.0e}".format(lr)
    # max_epochs = str(train_cfg['max_epochs'])
    # T_max = str(param_scheduler[0]['T_max'])
    # eta_min = param_scheduler[0]['eta_min']
    # eta_min = "{:.0e}".format(eta_min)
    # 执行训练命令
    os.system(f"python tools/train.py configs/textrecog/{model}/{name}.py --work-dir /public/yuziyang/work_dirs/rec/new_dict/lines/{model}/{name}/ --amp")  # _maxepochs{max_epochs}_Tmax{T_max}_etamin{eta_min}_lr{lr}


if __name__ == "__main__":
    train()
#   --resume
