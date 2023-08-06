# -*- coding: utf-8 -*-
"""
Created on Tue May 11 13:00:30 2021

@author: Abdussalam Aljbri
"""

import re
from time import perf_counter
#from os import _exit as exit

class quota:
    '''
    The time has to be passed as (\d\w)  Digits(d) for the time and one character(c) to represent the time period
    * s Seconds
    * m Minutes
    * h Hours
    * d Days
    
    quota_time: type (str) defualt value (6h) : represent the quota time for the session
    gap_time: type (str) defualt value (30m) : represent the time gap between the quota limit and the actual closing time for the session
        
    '''
    def __init__(self,quota_time:str = '6h', gap_time:str='30m'):
        
        self.start_time = perf_counter()
        self.quota_time = self._toSeconds(quota_time)
        self.gap_time = self._toSeconds(gap_time)
    
    def hastime(self)->bool:
        elapsed_time = self.quota_time - (perf_counter() - self.start_time)
        return (elapsed_time and elapsed_time >= self.gap_time)
    
    def time_up(self) -> bool:
        elapsed_time = self.quota_time - (perf_counter() - self.start_time)
        return not (elapsed_time and elapsed_time >= self.gap_time)
        
    
    def _toSeconds(self, wTime:str) -> int:
        d = 0
        t = 0
        tp = re.findall('[a-zA-Z]',wTime)
        if tp:
            tp = tp[0].lower()
        if tp.startswith('s'):
            d = 1
        elif tp.startswith('m'):
            d =  60
        elif tp.startswith('h'):
            d = 3600
        elif tp.startswith('d'):
            d = 86400
        else:
            d = 0
        tp = re.findall('[0-9]+',wTime)
        if tp:
            t = int(tp[0])
        return d * t