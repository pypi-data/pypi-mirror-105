# csbuilder
The framework supports you to build complex Client-Server applications.

# How to build
Our library is only supported by Python 3. Now we test it only on Python 3.7.1. If you meet any problems, even if with other versions, you could [create an issue](https://github.com/huykingsofm/csbuilder/issues) to notify us. We will solve them as quickly as possible.  

## Create Virtual Environment (optional but IMPORTANT)
*If you had your virtual environment, you can ignore this step.* 

You ought to create a virtual environment to avoid conflicting with other applications on your machine when installing our module. The virtual environment must be installed with [Python 3](https://www.python.org/downloads).  
I highly recommend you to use [Anaconda](https://www.anaconda.com/products/individual) because of its utilities. The command of creating a virtual environment in Anaconda is:
```bash
$ conda create -n your_venv_name
$ conda activate your_venv_name
(your_venv_name) $ _ 
```

Or use `Python venv`:
```bash
$ python -m venv path/to/your/venv
$ path/to/your/venv/Scripts/activate.bat
(your_venv_name) $ _
```

## Method 1: Install the PyPI version (not completed yet)
```bash
(your_venv_name) $ pip install csbuilder
```

## Method 2: Install the newest version (recommendation)

```bash

(your_venv_name) $ git clone https://github.com/huykingsofm/csbuilder.git
(your_venv_name) $ cd csbuilder
(your_venv_name) csbuilder $ pip install -e .
```

# How to use
Just use `import` statement and enjoy it. We will write documentation and tutorials as soon as possible so that you can understand our library easier.

```python
from csbuilder.listener import Listener
from csbuilder.client import ClientResponser
```

# Example
See the library [sft](https://github.com/huykingsofm/sft) supporting file transfer using `csbuilder`.