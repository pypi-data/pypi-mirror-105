# fastargs

Python library for argument and configuration management.

The goal of this library is to enable easy configuration of large code bases with many parameters. It should be particulary useful in machine learning applications with many hyper-parameters scattered across multiple files and components.

## Usage

### Install

1. PIP: `pip install fastargs`
2. Github: `pip install git+https://github.com/GuillaumeLeclerc/fastargs.git `

### Example
Simple full example available: https://github.com/GuillaumeLeclerc/fastargs/blob/main/examples/full_simple_example.py

### Declare the arguments

As demonstrated here you can declare your parameters in multiple files over your project. To make your code more readable it is recommended to declare the parameters as close as from where they are used.

In `train.py`:
```python
from fastargs import Section, Param
from fastargs.validation import InRange, And

Section("training.optimizer", "Optimizer parameters").params(
  learning_rate=Param(float, required=True),  # One can use simple type declaration
  momentum=Param(And(float, InRange(min=0)), default=0)  # Or more constrained validation rules
)

# The training code (see later sections on how to read the params)
```
In `dataloading.py`:
```python
from fastargs import Section, Param
from fastargs.validation import InRange, And

Section("data.loading", "Optimizer parameters").params(
  batch_size=Param(And(int, InRange(min=1)), required=True),
  num_workers=Param(And(int, InRange(min=0)), default=0)
)

# Data loading code
```

### Populate the arguments

Arguments can be defined from multiple sources (see below). They are not exclusive and can be mix and matched.
If a new source is added it overrides the previous one if a given argument was already defined.

In `main.py`:
```python
import argparse

# Import the rest of your code that declares the arguments
from fastargs import get_current_config

config = get_current_config()

# Option 1: From code
# -------------------

config.collect({
  'training.optimizer.learning_rate': 0.01,  # One can specify the path to arguments with dot notation
  'training.optimizer.momentum': 0.9,
  'data': {
    'loading': {
      'batch_size': 512  # One can have the structure explicit
    }
    'loading.num_workers': 10  # Or even a mix of both
  }
})


# Option 2: From a config file (yaml, json)
# -----------------------------------------

# Similarly one can use dot notation for arguments or use explicit structure (as shown in Option 1)
config.collect_config_file('./config.yaml')
config.collect_config_file('./config.json')


# Option 3: From env variables
# ----------------------------

# One can declare the env variables this way (bash)
# training.optimizer.momentum=0.9 python main.py
# OR
# export training.optimizer.momentum=0.9
# python main.py

config.collect_env_variables()


# Option 4: using argparse
# ------------------------

parser = argparse.ArgumentParser(description='fastargs demo')
config.augment_argparse(parser)
config.collect_argparse_args(parser)

# This will integrate fastargs with argparse
# It will:
# - Add a CLI argument for each fastargs argument
# - Generate a user friendly --help message
# - Allow the user to pass config files through CLI arguments and collect them aumatically for you
# - collect env variables
#
# Priority for duplicated parameters is: env variable, cli argument, config files from last to first
```

### Validating the arguments

Arguments are validated as you access them (see next section). However if you want to check all arguments at once you can do it too.

```python

# Option 1
# --------

errors = config.validate(mode='errordict')
# This will return you a dict where the keys are the parameters
# and the value the corresponding errors

# Option 2
# --------

config.validate(mode='stderr')
# If errors are found it will print a nice table summarizing all the errors 
# for the user and quit the program to let him fill the invalid/missing arguments

```

### Summary of parameters

You can produce a summary of the arguments defined:

```python
config.summary() 
# by default it will be written to stderr but you can change that by passing a file
# to the function
```

### Accessing arguments

#### Option 1: Explicitely

```python
# One can read individual arguments

config['training.optimizer.learning_rate']

# Or gather all arguments in a single object
arguments = config.get()
print(arguments.training.optimizer.learning_rate)
```

#### Option 2: Through decorators

It is possible to automatically feed arguments to functions without having to explicitely use the API of `fastargs`.


```python
from fastargs.decorators import param, section

@param('training.optimizer.learning_rate')
@param('training.optimizer.momentum')
def train_my_model(model, learning_rate, momentum):
  ### train your model
  
# To avoid repeating long path we offer the @section decorator

@section('training.optimizer')
@param('learning_rate')
@param('momentum')
def train_my_model(model, learning_rate, momentum):
  ### train your model
  
# Note that if one does:
train_my_model(model, learning_rate=10)
# the learning from the config will be ignored
# (but momentum will be since it wasn't explicitely overriden)
```

By default the parameter will be passed to the argument with name the last component of the path (eg. `a.b.c` -> `c`). However, it is possible that multiple parameter section share some parameter names. It is therefore possible to explicitely chose the name of the argument:

```python
@param('a.b.c', 'param1')
@param('d.e.c', 'param2')
def compute(param1, param2):
  pass # ....
```
### Advanced features

#### Argparse binary flags

For binary parameters in CLI arguments it is common to simply pass the name of argument with no value. We allow it using the following syntax:

```python
Section('test').params(
    p1=Param(bool, is_flag=True)
)
```

When collecting values with argparse one should simply use `--test.p1` to set the value to true. Not passing it will be equivalent to passing `False`. Note that this has no impact on other collection sources (python object, config files).


#### Modules as arguments

We wanted to give the ability to define parameters of type "Module". These arguments represent paths to an importable python module (eg. `torch.optim`). The goal is to automatically load code based on the arguments provided by the user and pass the module directly to the code that needs it.

Since imported modules can also define configuration/parameters we make sure to load them and add them to the documentation and let the user define them too

Example (from the tests):
```python
Section('module.import').params(
    module=Param(Module(), required=True)
)

cfg = get_current_config().collect({
    'module.import.module': 'test_module.with_params',
     # We assume that this parameter is declared in the module loaded above
    'imported_section.blah.p1': 42.5
})

loaded_module = cfg['module.import.module']
# If test_module.with_params has a function testme it becomes available
# directly in the content of the configuration object
loaded_module.testme()

# The parameter declared in the imported module is
# also loaded.
print(cfg['imported_section.blah.p1'])  # => 42.5
```

If we need to get a variable/function/class, we can use the import type `ImportedObject`. In the the case of the previous example, the user would have to pass `test_module.with_params.testme`, and the value in the configuration object would be the function itself and not the whole module.

#### Conditional sections

It is pretty common to have parameters that only makes sense if another parameter is defined and/or has a specific value. For example, in the context of optimization, stochastic gradient descent only has one parameter `learning_rate`. But if we use `Adam` we have extra parameters. In this situation one can do the following:

```python
Section('optim').params(
  algorithm=Param(str)
)

Section('optim.alpha').enable_if(labmda cfg: cfg['optim.algorithm'] == 'Adam').params(
  'momentum': Param(float, required=True),
  'alpha': Param(float, default=1.0),
  'beta': Param(float, default=1.0)
)
```
This way users won't see the option `momentum` until they define `optim.algorithm=Adam` and the momentum will not trigger validation error if not filled if another optimizer is chosen.

## Tests

One can run the tests using:
```
python -m unittest discover tests
```
