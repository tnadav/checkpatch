import sys
import os
import subprocess

SOURCE_FILE_EXTENTIONS = [
    ".c",
    ".h",
]

IGNORE_LIST = [
    "SPDX_LICENSE_TAG",
]

def format_ignore_arg():
	return "--ignore={0}".format(",".join(IGNORE_LIST))

def sys_path():
    for p in os.environ['PATH'].split(":"):
        yield p

def locate_perl():
    for p in os.environ['PATH'].split(":"):
        perl_exe = os.path.join(p, 'perl')
        if os.path.isfile(perl_exe):
		return perl_exe

    raise RuntimeError("Couldn't locate perl executable!")

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

def checkdir(src_dir):

    files = list(checked_files(src_dir))
    if len(files) == 0:
        print("Nothing to do")
        return True

    args = [locate_perl(), locate_checkpatch(), "-f", "-no-tree",
            format_ignore_arg()]
    args.extend(files)
    exit_code = subprocess.call(args)
    return exit_code == 0
