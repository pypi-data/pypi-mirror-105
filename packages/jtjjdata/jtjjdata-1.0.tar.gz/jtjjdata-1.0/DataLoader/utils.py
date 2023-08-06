
from threading import Thread
from .tools import print_func_time
import pandas as pd

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
            df = pd.read_hdf(path,'data').reindex(indexloc,level = cindex_level).loc[:,fields]
            # df = pd.read_pickle(path).reindex(indexloc,level = cindex_level).loc[:,fields]
            # df = pd.read_hdf(path,'data')[fields]
            # df = df.loc[df.index.get_level_values(level = 0).isin(indexloc)]
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


