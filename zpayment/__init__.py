import re

VERSION = (0, 1, 0, "alpha")

PURSE_RE = re.compile(ur'^(?P<type>ZP)(?P<number>\d+)$')
WMID_RE = re.compile(ur'^(\d+)$')
