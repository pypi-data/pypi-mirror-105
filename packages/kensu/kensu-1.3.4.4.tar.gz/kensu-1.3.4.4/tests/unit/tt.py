import kensu.pandas as pd

def data_prep(data):
    import numpy as np
    import pandas as pd
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

#Init
from kensu.utils.kensu_provider import KensuProvider
kensu = KensuProvider().initKensu(process_name='Exercise 3',
                            user_name='Sammy',
                            code_location='https://gitlab.example.com',
                            init_context=True,
                            project_names=['O-Reilly'],
                            environment="Production",
                            report_to_file=True,
                            offline_file_name='log_pandas_example.log')

#Generic
import kensu.pandas as pd

customers_info = pd.read_csv('/Users/kensu/Customers/Kensu/Trial/data/predict/jan-customers-data.csv')
contact_info = pd.read_csv('/Users/kensu/Customers/Kensu/Trial/data/predict/jan-contact-data.csv')
business_info = pd.read_csv('/Users/kensu/Customers/Kensu/Trial/data/predict/jan-business-data.csv')

customer360 = customers_info.merge(contact_info,on='id')
jan = pd.merge(customer360,business_info)

jan_final=data_prep(jan)

import kensu.pickle as pk
model=pk.load(open('/Users/kensu/Customers/Kensu/Trial/demo/model_t2.cav','rb'))
predictions = model.predict(jan_final)

jan['predictions']=predictions
jan.to_csv('jan',index=False)