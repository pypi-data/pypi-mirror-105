
#%%
import os
import abc
import pandas as pd
from datetime import datetime
from .config import data_path
from .tools import print_func_time,to_intdate
aindex_member = os.path.join(data_path,r'AIndexMembers')
aindex_membercitics = os.path.join(data_path,r'AIndexMembersCITICS')

class BaseStatusInfoProvider(abc.ABC):

    @abc.abstractmethod
    def get_status_data(self,instruments,fields,start_date,end_date):
        raise NotImplementedError


class LocalIndexMemberProvider(BaseStatusInfoProvider):

    def get_status_data(self,datapath,indexcode,start_date =None,end_date = None):
       
        start_date,end_date = to_intdate(start_date),to_intdate(end_date)
        df = pd.read_hdf(os.path.join(datapath,'all.h5'),"data")
        try:
            df = df.loc[indexcode]
            df['outdate'].fillna(int(datetime.now().strftime("%Y%m%d")),inplace = True)
            if (start_date is not None) & (end_date is not None):
                df = df.loc[(df.indate <= end_date)&(df.outdate >= start_date)]
            return df.loc[indexcode]
        except KeyError:
            print('Index %s info not found'%indexcode)
            return pd.DataFrame()
    
    @print_func_time
    def index_member(self,indexcode,start_date =None,end_date = None):
        """ AIndexMembers """
        return self.get_status_data(aindex_member,indexcode,start_date,end_date)
    
    @print_func_time
    def index_member_citics(self,indexcode,start_date =None,end_date = None):
        """ AIndexMembersCITICS """
        return self.get_status_data(aindex_membercitics,indexcode,start_date ,end_date)

        
        
        