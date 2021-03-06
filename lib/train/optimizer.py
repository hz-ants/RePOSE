import torch
import adabound

_optimizer_factory = {
    'adam': torch.optim.Adam,
    'adabound': adabound.AdaBound,
    'sgd': torch.optim.SGD,
}


def make_optimizer(cfg, net):
    params = []
    lr = cfg.train.lr
    final_lr = cfg.train.final_lr
    weight_decay = cfg.train.weight_decay

    for key, value in net.named_parameters():
        if not value.requires_grad:
            continue
        params += [{"params": [value], "lr": lr, "weight_decay": weight_decay}]

    if 'adam' in cfg.train.optim:
        optimizer = _optimizer_factory[cfg.train.optim](
            params, lr, weight_decay=weight_decay)
    elif 'adabound' in cfg.train.optim:
        optimizer = _optimizer_factory[cfg.train.optim](
            params, lr=lr, final_lr=final_lr, weight_decay=weight_decay)
    else:
        optimizer = _optimizer_factory[cfg.train.optim](params,
                                                        lr,
                                                        momentum=0.9)

    return optimizer
