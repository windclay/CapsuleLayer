from torch.nn import Module

import capsule_layer as CL


class MultiStepRI(object):
    r"""Set the routing iterations of model which contains capsule layer to the initial iterations added
    by addition once the number of epoch reaches one of the milestones.

    Args:
        model (Module): Wrapped model
        milestones (list): List of epoch indices. Must be increasing
        addition (int): Additive factor of routing iterations addition
        verbose (bool): If ``True``, prints a message to stdout for each update

    Examples::
        >>> # Assuming model uses iterations = 3
        >>> # rl = 3    if epoch < 10
        >>> # rl = 5    if 10 <= epoch < 30
        >>> # rl = 7    if epoch >= 30
        >>> from capsule_layer import CapsuleLinear
        >>> model = CapsuleLinear(30, 8, 16, 20, share_weight=False)
        >>> scheduler = MultiStepRI(model, milestones=[10, 30], addition=2, verbose=False)
        >>> for epoch in range(50):
        ...     scheduler.step()
    """

    def __init__(self, model, milestones, addition=2, verbose=False):
        if not list(milestones) == sorted(milestones):
            raise ValueError('Milestones should be a list of increasing integers. Got {}', milestones)
        self.milestones = milestones

        if not isinstance(model, Module):
            raise TypeError('{} is not an Module'.format(type(model).__name__))
        self.model = model

        self.addition = addition
        self.verbose = verbose
        self.last_epoch = 0

    def step(self):
        epoch = self.last_epoch + 1
        if epoch in self.milestones:
            for name, module in self.model.named_modules():
                if isinstance(module, CL.CapsuleConv2d) or isinstance(module, CL.CapsuleLinear):
                    module.num_iterations += self.addition
                    if self.verbose:
                        print('Epoch {}: increasing module {}\' routing iterations to {}.'.
                              format(epoch, name if name != '' else type(module).__name__, module.num_iterations))
        self.last_epoch = epoch
