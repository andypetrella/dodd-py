import urllib3
urllib3.disable_warnings()
import os
import datetime

from src.utils import dodd, ts

import kensu.numpy as np
import kensu.pandas as pd
from kensu.utils.rule_engine import check_nrows_consistency

def set_up():
    url = os.environ.get("KENSU_URL", None)
    token = os.environ.get("KENSU_TOKEN", None)
    client = dodd(url=url, token=token, timestamp=ts())

# TODO => have a file on S3 with null values for "marital"
def copy(target_directory):
    set_up()

    marital = ["divorced", "single", "married", "unknown"]
    customers_info = pd.read_csv('./data/input/customers.csv')

    check_nrows_consistency()
    referenced = customers_info[customers_info["marital"].isin(marital)]

    referenced.to_json(target_directory + '/customers.json')

def pipeline(target_directory):
    set_up()

    customers_info = pd.read_csv('./data/input/customers.csv')
    contact_info = pd.read_csv('./data/input/contact.csv')
    business_info = pd.read_csv('./data/input/business.csv')
    
    customer360 = customers_info.merge(contact_info,on='id')
    month_data = pd.merge(customer360,business_info)
    month_data = pipeline_data_prep(month_data)
    
    # This is where consistency is requested to be checked (published and validated)
    check_nrows_consistency()
    
    month_data.to_csv(target_directory + '/data.csv',index=False)

def pipeline_data_prep(data):
    data['education']=np.where(data['education'] =='basic.9y', 'Basic', data['education'])
    data['education']=np.where(data['education'] =='basic.6y', 'Basic', data['education'])
    data['education']=np.where(data['education'] =='basic.4y', 'Basic', data['education'])

    cat = [i for i in ['job','marital','education','default','housing','loan','contact','month','day_of_week','poutcome'] if i in data.columns]

    data_dummy = pd.get_dummies(data,columns=cat)

    features=[i for i in ['euribor3m', 'job_blue-collar', 'job_housemaid', 'marital_unknown',
      'month_apr', 'month_aug', 'month_jul', 'month_jun', 'month_mar',
      'month_may', 'month_nov', 'month_oct', "poutcome_success"] if i in data_dummy.columns]

    data_final = data_dummy[features]
    return data_final