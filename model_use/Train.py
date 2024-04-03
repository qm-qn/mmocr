import os
from configs.textrecog._base_.schedules.plus_schedule_adamw_cos_6e import optim_wrapper, param_scheduler, train_cfg


def train():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    name = 'plus'
    total = name
    lr = optim_wrapper['optimizer']['lr']
    lr = "{:.0e}".format(lr)
    max_epochs = str(train_cfg['max_epochs'])
    T_max = str(param_scheduler[0]['T_max'])
    eta_min = param_scheduler[0]['eta_min']
    eta_min = "{:.0e}".format(eta_min)
    # 执行训练命令
    os.system(f"python tools/train.py configs/textrecog/aster/_base_aster_{name}.py --work-dir /public/yuziyang/work_dirs/rec/new_dict/lines/aster_{total}_maxepochs{max_epochs}_Tmax{T_max}_etamin{eta_min}_lr{lr}/ --amp")


if __name__ == "__main__":
    train()
#   --resume
