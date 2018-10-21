import sys
import os
import subprocess

SOURCE_FILE_EXTENTIONS = [
    ".c",
    ".h",
]

IGNORE_LIST = [
    "SPDX_LICENSE_TAG",
    "AVOID_EXTERNS",
]

def format_ignore_arg():
	return "--ignore={0}".format(",".join(IGNORE_LIST))

def sys_path():
    for p in os.environ['PATH'].split(":"):
        yield p

def locate_exe(exe_name):
    for p in os.environ['PATH'].split(":"):
        exe_path = os.path.join(p, exe_name)
        if os.path.isfile(exe_path):
		return exe_path

    raise RuntimeError("Couldn't locate {0} executable!".format(exe_name))

def locate_perl():
	return locate_exe("perl")

def locate_git():
	return locate_exe("git")

def locate_checkpatch():
    py_path = os.path.abspath(__file__)
    cp_path = os.path.join(os.path.dirname(py_path), "checkpatch.pl")

    if not os.path.isfile(cp_path):
        raise RuntimeError("Couldn't locate checkpatch.pl")

    return cp_path

def checked_files(src_dir):

    abs_src_dir = os.path.abspath(src_dir)

    for root, dirs, files in os.walk(abs_src_dir):
        for file_name in files:
            base, ext = os.path.splitext(file_name)

            if ext not in SOURCE_FILE_EXTENTIONS:
                continue

            yield os.path.join(abs_src_dir, root, file_name)

def checkfiles(files):
    if len(files) == 0:
        print("Nothing to do")
        return True

    args = [locate_perl(), locate_checkpatch(), "-f", "-no-tree",
            format_ignore_arg()]
    args.extend(files)
    exit_code = subprocess.call(args)
    return exit_code == 0

def checkdir(src_dir):

    files = list(checked_files(src_dir))
    return checkfiles(files)

def checkfile(file_path):
    return checkfiles([file_path])

def checkpatch(from_commit, to_commit):
    diff = subprocess.Popen([locate_git(), "diff", from_commit, to_commit],
                            stdout = subprocess.PIPE)
    checkpatch = subprocess.Popen([locate_perl(), locate_checkpatch(), "-no-tree",
                                   format_ignore_arg()], stdin = diff.stdout)
    diff.stdout.close()
    checkpatch.communicate()

    return checkpatch.returncode == 0
