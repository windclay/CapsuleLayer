# Capsule Layer
PyTorch Capsule Layer, the CapsuleConv2d is still on progress, it's not working now.

## Requirements
* [Anaconda(Python 3.6 version)](https://www.anaconda.com/download/)
* PyTorch(version >= 0.3.1)
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
from torch.autograd import Variable
from capsule_layer import capsule_cov2d
x = torch.randn(4, 8, 28, 50)
w = torch.randn(2, 2, 3, 5, 8, 4)
if torch.cuda.is_available():
    x = x.cuda()
    w = w.cuda()
# routing_type options: ['dynamic', 'contract', 'means', 'cosine', 'tonimoto', 'pearson']
y = capsule_cov2d(Variable(x), Variable(w), stride=1, padding=1, routing_type='dynamic')
```
or with modules interface:
```python
import torch
from torch.autograd import Variable
from capsule_layer import CapsuleConv2d
x = torch.randn(4, 8, 28, 50)
# routing_type options: ['dynamic', 'contract', 'means', 'cosine', 'tonimoto', 'pearson']
module = CapsuleConv2d(in_channels=8, out_channels=16, kernel_size=(3, 5), in_length=4, out_length=8, stride=1, padding=1, routing_type='means')
if torch.cuda.is_available():
    x = x.cuda()
    module.cuda()
y = module(Variable(x))
```

### CapsuleLinear
```python
import torch
from torch.autograd import Variable
from capsule_layer import capsule_linear
x = torch.randn(64, 128, 8)
w = torch.randn(10, 16, 8)
if torch.cuda.is_available():
    x = x.cuda()
    w = w.cuda()
# routing_type options: ['dynamic', 'contract', 'means', 'cosine', 'tonimoto', 'pearson']
y = capsule_linear(Variable(x), Variable(w), share_weight=True, routing_type='contract')
```
or with modules interface:
```python
import torch
from torch.autograd import Variable
from capsule_layer import CapsuleLinear
x = torch.randn(64, 128, 8)
# routing_type options: ['dynamic', 'contract', 'means', 'cosine', 'tonimoto', 'pearson']
module = CapsuleLinear(out_capsules=10, in_length=8, out_length=16, in_capsules=None, routing_type='contract', num_iterations=3)
if torch.cuda.is_available():
    x = x.cuda()
    module.cuda()
y = module(Variable(x))
```

### Routing Algorithm
* dynamic routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(64, 10, 128, 8)
if torch.cuda.is_available():
    x = x.cuda()
y = F.dynamic_routing(Variable(x), num_iterations=10)
```
* contract routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(64, 5, 64, 8)
if torch.cuda.is_available():
    x = x.cuda()
y = F.contract_routing(Variable(x), num_iterations=100)
```
* means routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(16, 10, 128, 8)
if torch.cuda.is_available():
    x = x.cuda()
y = F.means_routing(Variable(x), num_iterations=5)
```
* cosine routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(64, 10, 32, 8)
if torch.cuda.is_available():
    x = x.cuda()
y = F.cosine_routing(Variable(x), num_iterations=20)
```
* tonimoto routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(8, 5, 32, 8)
if torch.cuda.is_available():
    x = x.cuda()
y = F.tonimoto_routing(Variable(x), num_iterations=4)
```
* pearson routing
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x = torch.randn(7, 10, 64, 16)
if torch.cuda.is_available():
    x = x.cuda()
y = F.pearson_routing(Variable(x), num_iterations=12)
```

### Similarity Algorithm
* tonimoto similarity
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x1 = torch.randn(64, 16)
x2 = torch.randn(1, 16)
if torch.cuda.is_available():
    x1 = x1.cuda()
    x2 = x2.cuda()
y = F.tonimoto_similarity(Variable(x1), Variable(x2), dim=-1)
```
* pearson similarity
```python
import torch
from torch.autograd import Variable
import capsule_layer.functional as F
x1 = torch.randn(32, 8, 16)
x2 = torch.randn(32, 8, 1)
if torch.cuda.is_available():
    x1 = x1.cuda()
    x2 = x2.cuda()
y = F.pearson_similarity(Variable(x1), Variable(x2), dim=1)
```

## Contribution
Any contributions to Capsule Layer are welcome!

## Copyright and License
Capsule Layer is provided under the [MIT License](LICENSE).