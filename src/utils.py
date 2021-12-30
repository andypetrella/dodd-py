import urllib3
urllib3.disable_warnings()
import os
import datetime
import logging

from kensu.utils.kensu_provider import KensuProvider
from kensu.utils.reporters import ApiReporter, LoggingReporter

def dodd(url, token, timestamp, reporter=LoggingReporter, file_name="dodd.log", **kwargs):
    if "CONF_FILE" not in os.environ:
        logging.warning("Forcing CONF_FILE var env to 'conf.ini'")
        os.environ["CONF_FILE"] = "./src/conf.ini"

    if "ENV" in os.environ:
        environment = os.environ["ENV"]
        reporter = ApiReporter
    else:
        environment = "Local"

    with open('./src/conf.ini.template', "r") as r:
         with open("./src/conf.ini", "w") as w:
            from string import Template
            s = Template(r.read())
            w.write(s.substitute(url=url or '', token=token or ''
                                , environment=environment
                                , timestamp=timestamp or ts()
                                , reporter=reporter.__name__
                                , file_name=file_name or ''))
    
    kp = KensuProvider()
    k = kp.initKensu(allow_reinit=True, **kwargs)
    return k

def ts(year=None, month=None, date=None):
    if year is not None and month is not None and date is not None:
        t = datetime.datetime(year,month,date).timestamp()
    else: 
        t = datetime.datetime.now().timestamp()
    return round(t)*1000