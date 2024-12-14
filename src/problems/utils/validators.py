from django.http import HttpResponse

modules = [
    "open",
    "os",
    "shutil",
    "subprocess",
    "socket",
    "time",
    "datetime",
    "configparser",
    "ctypes",
    "sys",
    "platform",
    "pathlib",
    "uuid",
    "hashlib",
    "sqlite3",
    "resource",
    "venv",
    "psutil",
    "signal",
    "futures",
    "getpass",
    "glob",
    "tempfile",
    "argparse",
    "multiprocessing",
    "threading",
    "inspect",
    "queue",
    "logging",
    "pdb",
    "tracemalloc",
    "unittest",
    "email",
    "http",
    "ftplib",
    "smtplib",
    "asyncio"
]


def validate_code(code):
    for i in modules:
        if i in code:
            return False, i
    return True, True
