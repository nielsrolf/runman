"""
python runman.py <path to executable> <name for this run> [-p python path] [programm args]
alias:
alias runman='python <path to this file>'
"""
import os
from pathlib import Path
import shutil
import sys
import pdb
import importlib.util
import numpy as np
import re
import subprocess

file_types = [".py", ".csv", ".xml", ".json"]


def copy_src_files(origin, current, to, executable):
    for file in current.iterdir():
        if re.match(r'config[0-9]*\.py', str(file)) and str(file) != str(executable):
            print("Skip config file "+str(file))
            continue
        print("Scanning "+str(file))
        if file.is_file() and file.suffix in file_types:
            relative = file.relative_to(origin)
            target = to / relative
            target_dir = target.parent

            if not target_dir.exists():
                print("mkdir ", target_dir)
                target_dir.mkdir(parents=True)
            shutil.copyfile(str(file), target)
        if file.is_dir():
            copy_src_files(origin, file, to, executable)


def new_run(executable, name, args, python):
    # copy executables
    executable = Path(executable)
    src, entry = executable.parent, executable.name
    target = src / "../runs" / name
    copy_src_files(src, src, target, executable)
    # exec file
    os.chdir(target)
    os.system("echo {} {} {} > again.sh".format(python, entry, " ".join(args)))
    # os.system("{} {} {}".format(python, entry, " ".join(args))) # > logs.txt 2> logs_error.txt
    with open("logs.txt", "w") as logfile:
        proc = subprocess.Popen([python, entry]+args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            line = line.decode('utf-8')
            sys.stdout.write(line)
            logfile.write(line)


def runmanager():
    executable, name = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == "p":
        python = sys.argv[4]
        args = sys.argv[4:]
    else:
        python = "python"
        args = sys.argv[3:]

    new_run(executable, name, args, python)


def makeconfigs():
    # python runman.py makeconfigs <template> <options>

    def load(path):
        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    template_name, options = sys.argv[2], load(sys.argv[3])
    var_names = list(options.all.keys())
    options_count = np.prod([len(values) for values in options.all.values()])

    def write_config(choices, config_id):
        config_str = ""
        for var_name, val in choices.items():
            config_str += "{} = {} \n".format(var_name, val)
        with open(template_name, "r") as template:
            with open("config{}.py".format(config_id), "w") as out:
                for line in template:
                    out.write(line.replace("<config>", config_str))
    
    def descriptive_name(choices):
        def to_name(value):
            value = re.sub("\(.*\)", "", value)
            value = re.sub("\[.*\]", "", value)
            value = value.replace(" ", "")
            value = value.replace("'", "")
            value = value.replace("\"", "")
            return value
        name = "-".join([to_name(value) for value in choices.values()])
        return name

    for config_id in range(options_count):
        choices = {}
        number = config_id
        for var in var_names:
            choice_id = number % len(options.all[var])
            number = int((number - choice_id)/len(options.all[var]))
            choices[var] = options.all[var][choice_id]
        write_config(choices, config_id)
        print("runman config{}.py {}".format(config_id, descriptive_name(choices)))





if sys.argv[1] == "makeconfigs":
    makeconfigs()
else:
    runmanager()
