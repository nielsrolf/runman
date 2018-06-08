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
`alias runman='<path to runman.py>'`


## TODO
- Real argument parser