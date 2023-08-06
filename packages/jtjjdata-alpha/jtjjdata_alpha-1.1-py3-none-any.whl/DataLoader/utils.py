
from threading import Thread
from .tools import print_func_time,bisect_right,bisect_left,to_intdate
from .config import data_path

import pandas as pd
import numpy as np
import h5py
import os

class Mythread(Thread):

    def __init__(self,target,args,name = '',**kwargs):
        Thread.__init__(self)
        self._target = target
        self._args = args
        self._kwargs = kwargs

    @property
    def result(self):
        return getattr(self,'_result',None)
    
    def run(self):
        """Method representing the thread's activity."""
        try:
            if self._target:
                self._result = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

class BatchH5Reader:

    @staticmethod
    def read_h5_m(path,indexloc,fields,cindex_level):
        try:
            # df = pd.read_hdf(path,'data').reindex(indexloc,level = cindex_level).loc[:,fields]
            # df = pd.read_pickle(path).reindex(indexloc,level = cindex_level).loc[:,fields]
            df = pd.read_hdf(path,'data')[fields]
            df = df.loc[df.index.get_level_values(level = cindex_level).isin(indexloc)]
        except FileNotFoundError:
            df = pd.DataFrame(columns=fields)
        return df
    
    @staticmethod
    def read_h5_s(path,indexloc,fields):
        df = pd.read_hdf(path,'data').reindex(indexloc)[fields]
        return df
    
    @print_func_time
    def batch_reader(self,pathlist,instruments,fields,reader = 'read_h5_m',cindex_level = 0):
        Threads = []
        for path in pathlist:
            Threads.append(Mythread(target = getattr(BatchH5Reader,reader),args = (path,instruments,fields,cindex_level)))
        for thread in Threads:
            thread.start()
        for thread in Threads:
            thread.join()
        dfs = [thread.result for thread in Threads if not thread.result.empty]
        return dfs
    
class CalendarD:

    def __init__(self,caltype):
        """
            params:
                caltype: str ['Tdays','Fdays']
        """
        self.path = os.path.join(data_path,'calendar',caltype + '.txt')
        self.cal = pd.read_csv(self.path, names=['dt'])['dt']
        self.rcal = self.cal.reset_index().set_index('dt') 
    
    def get_calendar(self,start_date,end_date):
        return self.cal.loc[(self.cal>=start_date)&(self.cal<=end_date)]
    
    def get_index(self,start_date,end_date):
        if isinstance(start_date,str):
            start_date = to_intdate(start_date)
        if isinstance(end_date,str):
            end_date = to_intdate(end_date)
        try:
            start_index = int(self.rcal.loc[start_date].values)
        except:
            start_index = bisect_left(self.cal,start_date)
        try:
            end_index = int(self.rcal.loc[end_date].values)
        except:
            end_index = bisect_right(self.cal,end_date) - 1
        return start_index,end_index


def read_mergeh5(path,ori_instruments,fields,start_index,end_index,tidx = 'trade_dt'):
    instruments = [''.join(inst.split('.')[::-1]) for inst in ori_instruments]
    with h5py.File(path,'r') as h5:
        instlist = h5['instlist'][:].astype(str)            # inst code list
        instloc = h5['instloc'][:]     
        rsilist = h5['rsilist'][:]
        reilist = h5['reilist'][:]  
        dset = h5['data']  
        cidx = dset.shape[0]  
        
        infoloc = np.where(np.in1d(instlist,instruments))
        availbles = np.array(ori_instruments)[np.where(np.in1d(instruments,instlist))[0]]
        mask,amount = gen_idxs(cidx,infoloc,instloc,rsilist,reilist,start_index,end_index)

        if fields:
            data = dset[(mask,tidx,*fields)]
        else:
            data = dset[mask]

        data = pd.DataFrame(data)
        data['code'] = np.repeat(availbles,amount)
        return data

def gen_idxs(cidx,infoloc,instloc,rsilist,reilist,start_index,end_index):
    mask = np.zeros(cidx,dtype = bool)
    amount = []
    for i in infoloc[0]:
        instsiloc = instloc[i]
        tsi,tei = max(start_index - rsilist[i],0), min(end_index - rsilist[i], reilist[i] - rsilist[i])
        h5si,h5ei = tsi + instsiloc,tei + instsiloc
        amount.append(h5ei - h5si + 1)
        mask[h5si:h5ei + 1] = True
    return mask,amount


Tcal = CalendarD('Tdays')