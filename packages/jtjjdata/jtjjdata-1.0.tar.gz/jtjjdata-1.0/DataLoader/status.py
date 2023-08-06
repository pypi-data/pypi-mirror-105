
#%%
import os
import abc
import pandas as pd
from .config import data_path
from .tools import print_func_time,to_intdate
aindex_member = os.path.join(data_path,r'AIndexMembers')
aindex_membercitics = os.path.join(data_path,r'AIndexMembersCITICS')

class BaseStatusInfoProvider(abc.ABC):

    @abc.abstractmethod
    def get_status_data(self,instruments,fields,start_date,end_date):
        raise NotImplementedError


class LocalStatusInfoProvider(BaseStatusInfoProvider):

    def get_status_data(self,datapath,instruments,fields,start_date =None,end_date = None):
        if isinstance(instruments,str):
            instruments = [instruments,]

        df = pd.read_hdf(os.path.join(datapath,'all.h5'),"data").reindex(instruments)
        if fields:
            df = df[fields]
        return df
    
    def index_member(self,instruments,fields,start_date,end_date):
        return self.get_status_data(aindex_member,instruments,fields,start_date,end_date)
    
    def index_member_citics(self,instruments,fields,start_date,end_date):
        return self.get_status_data(aindex_membercitics,instruments,fields,start_date,end_date)

        
