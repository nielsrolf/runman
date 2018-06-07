# runman
Module to handle programms that will run with different options. Makes experiments easier to reproduce.

For convenient use, set an alias:
`alias runman='<path to runman.py>'`

## Generate configs
`runman makeconfigs <template> [-p <pythonpath>] <options>`

## Start run
`runman <python file> <run name> [args]`

## TODO
Better argument parser
Save args, generate .sh that executes exactly the same
Log output