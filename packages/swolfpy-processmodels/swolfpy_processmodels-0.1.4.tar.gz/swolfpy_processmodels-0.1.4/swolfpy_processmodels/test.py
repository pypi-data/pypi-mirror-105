# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:20:29 2021

@author: msmsa
"""



import swolfpy_processmodels as sp
A= sp.WTE()
A.calc()
report=A.report()





import swolfpy_processmodels as sp
A= sp.SS_MRF()
A.calc()
report=A.report()




import swolfpy_processmodels as sp
A= sp.TS()
A.calc()
report=A.report()







import swolfpy_processmodels as sp
A= sp.Reproc()
A.calc()
report=A.report()











from time import time
start = time()
for i in range(100):
    A= sp.SS_MRF()
    A.calc()
    report=A.report()
print(time()-start)




import swolfpy_processmodels as sp
import pandas as pd
import numpy as np


scheme = sp.SF_Col.scheme()
scheme[('RWC', 'SSYW', 'SSR')] = 1
A = sp.SF_Col('SF', scheme)
A.calc()
report= A.report()




import swolfpy_inputdata as spid

data = spid.TS_Input()

