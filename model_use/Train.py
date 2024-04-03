import os


def train():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    name = 'IAM'
    total = name
    max_epochs = '288'
    T_max = '8'
    eta_min = '4e-6'
    lr = '2e-4'
    # 执行训练命令
    os.system(f"python tools/train.py configs/textrecog/aster/_base_aster_{name}.py --work-dir /public/yuziyang/work_dirs/rec/new_dict/lines/aster_{total}_maxepochs{max_epochs}_Tmax{T_max}_etamin{eta_min}_lr{lr}/ --amp --resume")


if __name__ == "__main__":
    train()
