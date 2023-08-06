__version__ = '0.7.0a0+f9ef235'
git_version = 'f9ef235c402f48a335293c626e17bd8504d3af87'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
