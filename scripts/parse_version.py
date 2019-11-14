#!/usr/bin/env python3
import re


with open("libra/version.py", "r") as fp:
    try:
        version = re.findall(
            r"^version = \"([0-9\.]+)\"", fp.read(), re.M
        )[0]
        print(version, end='')
        exit(0)
    except Exception:
        print("Error parsing libra version")
        exit(-1)

