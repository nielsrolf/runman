# runman
Module to handle programs that generate data. If you have an experiment that generates data, but the code is changing, old results may not be connected to the current state of the code anymore. For easier reproducability, runman copies all your source code into `../runs/<name you choose>`, executes the program there, saves the logs (also printed to stdout) and creates a file `again.sh` that contains the command that let's your program run in the exact same way - also with command line arguments.

## Start run
`runman <python file> <run name> [args]`

## Random seeds
Runman can also set random seeds for numpy (and scipy, which uses numpys random generator), tensorflow and Pythons random module.
In order to do this, place `<seeds>` in your main template, before the first random number is generated,
at a place where the code is not indented. It also has the following restrictions: `random` must be imported as `random`,
`numpy` as `np`and tensorflow as `tf`. You can change these conventions if you need at the beggining of the script.
Then run `runman makeconfigs <template> [<options>]`

## Manage different versions
I often run the same simulation with, say, three different neural networks, two data sets and two different noise levels. Runman can also handle this for you: you create one file that contains something like this:

```
all = {
    "nn": ["get_nn1()", "get_nn2()"],
    "data": ["Data(samples=1000)", "Data(samples=50000)"],
    "noise": ["0.5", "0.7"]
}
```

You load the settings in your program (template) by:

```
# your code
<config>
# more code
```

Then runman can generate you all the different versions of your program with the comman `runman makeconfigs <template> [-p <pythonpath>] <options>`. The generated files will have names like "config1.py" and be the same as `<template>`, only the config will be replaced:

```
# your code
nn = get_nn1()
data = Data(samples=1000)
noise = 0.5
# more code
```

Runman also suggets names for the directories for each generated config file that try to be descriptive.

## Setup

For convenient use, set an alias:
`alias runman='python <path to runman.py>`


## TODO
- Real argument parser

## Example
This is an example foor generating the configurated files in `examples/src`.

First, we generate the config files 
```
runman git:(master) ✗ cd example/src 
➜  src git:(master) ✗ runman makeconfigs random_distribution.py configs.py
runman config0.py 1-1
runman config1.py -2-1
runman config2.py 0.5-1
runman config3.py 1-2
runman config4.py -2-2
runman config5.py 0.5-2
runman config6.py 1-3
runman config7.py -2-3
runman config8.py 0.5-3
```

Then we run one of the configs, which will create a new folder in `../runs`

```
➜  src git:(master) ✗ runman config8.py 0.5-3                             
Scanning configs.py
mkdir  ../runs/0.5-3
Scanning config8.py
Skip config file config3.py
Skip config file config7.py
Skip config file config6.py
Scanning __pycache__
Scanning __pycache__/configs.cpython-36.pyc
Skip config file config2.py
Skip config file config5.py
Skip config file config1.py
Skip config file config0.py
Scanning random_distribution.py
Skip config file config4.py
```

Now, we can run the experiment again, and the plot doesn't change even though it's randomly generated.

```
➜  example git:(master) ✗ cd ../runs
➜  runs git:(master) ✗ cd 0.5-3
➜  0.5-3 git:(master) ✗ source again.sh
```