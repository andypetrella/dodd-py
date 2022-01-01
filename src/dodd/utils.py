import urllib3
urllib3.disable_warnings()
import os
import datetime
import logging

from kensu.utils.kensu_provider import KensuProvider
from kensu.utils.reporters import ApiReporter, LoggingReporter

def client(timestamp=None, **kwargs):
    url = os.environ.get("KENSU_URL", None)
    token = os.environ.get("KENSU_TOKEN", None)
    sdk_url = os.environ.get("KENSU_SDK_URL", None)
    sdk_pat = os.environ.get("KENSU_SDK_PAT", None)
    if sdk_url is not None and sdk_pat is not None:
        sdk = f'sdk_url={sdk_url}\nPAT={sdk_pat}'
    else:
        sdk = ''
        
    if timestamp is None:
        timestamp = ts()

    if "CONF_FILE" not in os.environ:
        logging.warning("Forcing CONF_FILE var env to 'conf.ini'")
        os.environ["CONF_FILE"] = "./src/conf.ini"

    if "ENV" in os.environ:
        environment = os.environ["ENV"]
        if "KENSU_REPORTER" in os.environ:
            reporter = os.environ["KENSU_REPORTER"]
        else:
            reporter = ApiReporter.__name__
    else:
        environment = "Local"
        reporter = LoggingReporter.__name__

    with open('./src/conf.ini.template', "r") as r:
         with open("./src/conf.ini", "w") as w:
            from string import Template
            s = Template(r.read())
            w.write(s.substitute(url=url or '', token=token or ''
                                , sdk=sdk
                                , environment=environment
                                , timestamp=timestamp or ts()
                                , reporter=reporter
                                , file_name="dodd.log"))
    
    kp = KensuProvider()
    k = kp.initKensu(allow_reinit=True, **kwargs)
    return k

def ts(year=None, month=None, date=None):
    if year is not None and month is not None and date is not None:
        t = datetime.datetime(year,month,date).timestamp()
    else: 
        t = datetime.datetime.now().timestamp()
    return round(t)*1000