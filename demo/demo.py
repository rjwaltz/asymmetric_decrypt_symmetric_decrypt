import click
import json
import os.path
import os
import collections
import functools
import re
import sys
from datetime import datetime
import traceback
import zipfile




class Exam_JSON:
    ...



class Enc_Handler:
    "handle the .enc file"

    def __init__(self, path):
        ...

    def unzip(src, dest):
        ...


class Report_Handler:
    "handle the cipher or plain report pdf"

    def __init__(self, path):
        ...


@click.command()
@click.option("--enc", "-en", default=os.path.abspath("."),
            help="")
@click.option("--creport", "-cr", prompt="The report path",
            help="")
@click.option("--monitoring", "-m", prompt="The connect monitoring path",
            help="")
def main(enc, report, monitoring):
    
    try:
        os.mkdir(os.path.join(os.path.abspath("."), "tmp"))
    except FileExistsError:
        pass
    
    enc = enc.replace("\\", "").strip()
    report = report.replace("\\", "").strip()
    monitoring = monitoring.replace("\\", "").strip()

    assert os.path.isdir(monitoring), "\033[1;31mOops, <%s> is not a folder.\033[0m" % monitoring
    assert json.endswith(".enc"), "\033[1;31mOops, it's not a enc file.\033[0m"



if __name__=="__main__":
    main()