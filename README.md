# Capsule Layer
PyTorch Capsule Layer.

## Requirements
* [Anaconda](https://www.anaconda.com/download/)
* PyTorch
```
conda install pytorch torchvision -c pytorch
```

## Installation
```
pip install git+https://github.com/leftthomas/CapsuleLayer.git@master
```
To update:
```
pip install --upgrade git+https://github.com/leftthomas/CapsuleLayer.git@master
```

## Examples
### CapsuleConv2d
```python
import torch
from capsule_layer import capsule_cov2d
x = torch.randn(4, 8, 28, 50)
w = torch.randn(2, 8, 4, 3, 5)
if torch.cuda.is_available():
    x, w = x.to('cuda'), w.to('cuda')
# routing_type options: ['dynamic', 'k_means']
y = capsule_cov2d(x, w, stride=1, padding=1, routing_type='k_means')
```
or with modules interface:
```python
import torch
from capsule_layer import CapsuleConv2d
x = torch.randn(4, 8, 28, 50)
module = CapsuleConv2d(in_channels=8, out_channels=16, kernel_size=(3, 5), in_length=4, out_length=8, stride=1, padding=1, routing_type='k_means', bias=False)
if torch.cuda.is_available():
    x, module = x.to('cuda'), module.to('cuda')
y = module(x)
```

### CapsuleConvTranspose2d
```python
import torch
from capsule_layer import capsule_conv_transpose2d
x = torch.randn(20, 16, 50, 100)
w = torch.randn(4, 4, 8, 3, 5)
if torch.cuda.is_available():
    x, w = x.to('cuda'), w.to('cuda')
# routing_type options: ['dynamic', 'k_means']
y = capsule_conv_transpose2d(x, w, routing_type='k_means')
```
or with modules interface:
```python
import torch
from capsule_layer import CapsuleConvTranspose2d
x = torch.randn(20, 16, 50, 100)
module = CapsuleConvTranspose2d(in_channels=16, out_channels=32, kernel_size=(3, 5), in_length=4, out_length=8, bias=False)
if torch.cuda.is_available():
    x, module = x.to('cuda'), module.to('cuda')
y = module(x)
```

### CapsuleLinear
```python
import torch
from capsule_layer import capsule_linear
x = torch.randn(64, 128, 8)
w = torch.randn(10, 16, 8)
if torch.cuda.is_available():
    x, w = x.to('cuda'), w.to('cuda')
# routing_type options: ['dynamic', 'k_means']
y = capsule_linear(x, w, share_weight=True, routing_type='dynamic', dropout=0.5)
```
or with modules interface:
```python
import torch
from capsule_layer import CapsuleLinear
x = torch.randn(64, 128, 8)
module = CapsuleLinear(out_capsules=10, in_length=8, out_length=16, in_capsules=None, routing_type='dynamic', num_iterations=3, dropout=0.5, bias=False)
if torch.cuda.is_available():
    x, module = x.to('cuda'), module.to('cuda')
y = module(x)
```

### Routing Algorithm
* dynamic routing
```python
import torch
import capsule_layer.functional as F
x = torch.randn(64, 10, 128, 8)
if torch.cuda.is_available():
    x = x.to('cuda')
y, prob = F.dynamic_routing(x, num_iterations=10, squash=False, return_prob=True)
```
* k-means routing
```python
import torch
import capsule_layer.functional as F
x = torch.randn(64, 5, 64, 8)
if torch.cuda.is_available():
    x = x.to('cuda')
# similarity options: ['dot', 'cosine', 'tonimoto', 'pearson']
y = F.k_means_routing(x, num_iterations=100, similarity='tonimoto')
```

### Similarity Algorithm
* tonimoto similarity
```python
import torch
import capsule_layer.functional as F
x1 = torch.randn(64, 16)
x2 = torch.randn(1, 16)
if torch.cuda.is_available():
    x1, x2 = x1.to('cuda'), x2.to('cuda')
y = F.tonimoto_similarity(x1, x2, dim=-1)
```
* pearson similarity
```python
import torch
import capsule_layer.functional as F
x1 = torch.randn(32, 8, 16)
x2 = torch.randn(32, 8, 1)
if torch.cuda.is_available():
    x1, x2 = x1.to('cuda'), x2.to('cuda')
y = F.pearson_similarity(x1, x2, dim=1)
```

### Dynamic Scheduler
* routing iterations
```python
from capsule_layer import CapsuleLinear
from capsule_layer.optim import MultiStepRI
model = CapsuleLinear(3, 4, 7, num_iterations=2)
scheduler = MultiStepRI(model, milestones=[5, 20], addition=3, verbose=True)
# scheduler = MultiStepRI(model, milestones=[5, 20], addition=[3, 3], verbose=True)
for epoch in range(30):
    model.train()
    ...
    model.eval()
    ...
    scheduler.step()
```
* dropout
```python
from capsule_layer import CapsuleLinear
from capsule_layer.optim import MultiStepDropout
model = CapsuleLinear(3, 4, 7, dropout=0.1)
scheduler = MultiStepDropout(model, milestones=[5, 20], addition=0.3, verbose=True)
# scheduler = MultiStepDropout(model, milestones=[5, 20], addition=[0.3, 0.3], verbose=True)
for epoch in range(30):
    model.train()
    ...
    model.eval()
    ...
    scheduler.step()
```

## Contribution
Any contributions to Capsule Layer are welcome!

## Copyright and License
Capsule Layer is provided under the [MIT License](LICENSE).