#!/usr/bin/env python3
#export TESTBENCH_HOME=/home/dmd/Workplace/HiMap
import numpy as np
import sys
import os
import os.path
import math
import matplotlib
#import run_morpher_edn
import time
import pandas as pd
import datetime

matplotlib.use('Agg')
import matplotlib.pyplot as plt


himap2_config = pd.read_csv("himap2_config_v2.csv")
himap2_legacy_config = pd.read_csv("legacy_config_v2.csv")
himap2_config_entry_id_list = []
legacy_config_entry_id_list = []

print(himap2_config)
print(himap2_legacy_config)

HIMAP2_HOME = '/home/dmd/Workplace/HiMap2'
print(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M"))	

if True:
  # ## Run design space exploration
  print("Running HiMap2 Compiler")
  entry_id = 0
  for i, j in himap2_config.iterrows():
      #print('i: %s' % i)
      #print('j: %s' %j)
      if j["Entry_ID"] in himap2_config_entry_id_list:	  
      	os.chdir(HIMAP2_HOME+'/HiMap2_Scripts/'+j["Application"])
      	#os.system('pwd')
      	print('python run_morpher_%s.py  %s %s %s %s %s %s %s %s %s %s %s %s %s %s &' % (j["Application"],j["N"],j["init"], j["C1"],j["C2"],j["r"],j["c"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],j["Entry_ID"],j["summarylog"], j["initII"], j["maxIterTime"]))
      #if True:
      	os.system('python run_morpher_%s.py  %s %s %s %s %s %s %s %s %s %s %s %s %s %s &' % (j["Application"],j["N"],j["init"], j["C1"],j["C2"],j["r"],j["c"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],j["Entry_ID"], j["summarylog"], j["initII"], j["maxIterTime"]))
  

if True:
  # ## Run design space exploration
  print("Running Legacy Compiler")
  #entry_id = 0
  for i, j in himap2_legacy_config.iterrows():
  	#pass
    if j["Entry_ID"] in legacy_config_entry_id_list:	 
    	os.chdir(HIMAP2_HOME+'/HiMap2_Scripts/'+j["Application"])
    	print('python run_morpher_%s_legacy.py %s %s %s %s %s %s %s %s &' % (j["Application"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],j["Entry_ID"], j["summarylog"], j["initII"], j["maxIterTime"]))
    #if True:
    	os.system('python run_morpher_%s_legacy.py %s %s %s %s %s %s %s %s &' % (j["Application"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],j["Entry_ID"], j["summarylog"], j["initII"], j["maxIterTime"]))
