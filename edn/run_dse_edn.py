#!/usr/bin/env python3
#export TESTBENCH_HOME=/home/dmd/Workplace/HiMap
import numpy as np
import sys
import os
import os.path
import math
import matplotlib
import run_morpher_edn
import time
import pandas as pd
import datetime

matplotlib.use('Agg')
import matplotlib.pyplot as plt


himap2_config = pd.read_csv("config_himap.csv", index_col ="Application")
himap2_legacy_config = pd.read_csv("legacy_config_himap.csv", index_col ="Application")

print(himap2_config)

HIMAP2_HOME = '/home/dmd/Workplace/HiMap2'	

if False:
  # ## Run design space exploration
  print("Design space exploration")
  entry_id = 0
  for i, j in himap2_config.iterrows():
      os.chdir(HIMAP2_HOME+'/HiMap2_Scripts')
      print('python run_morpher_edn.py  %s %s %s %s %s %s %s %s %s %s %s %s %s &' % (j["N"],j["init"], j["C1"],j["C2"],j["r"],j["c"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],entry_id,j["summarylog"], j["initII"]))
      if True:
        os.system('python run_morpher_edn.py  %s %s %s %s %s %s %s %s %s %s %s %s %s &' % (j["N"],j["init"], j["C1"],j["C2"],j["r"],j["c"],j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],entry_id, j["summarylog"], j["initII"]))
      entry_id = entry_id+1

if True:
  # ## Run design space exploration
  print("Design space exploration")
  entry_id = 0
  for i, j in himap2_legacy_config.iterrows():
      os.chdir(HIMAP2_HOME+'/HiMap2_Scripts')
      print('python run_morpher_edn_legacy.py %s %s %s %s %s %s %s &' % (j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],entry_id, j["summarylog"], j["initII"]))
      if True:
        os.system('python run_morpher_edn_legacy.py %s %s %s %s %s %s %s &' % (j["arch_desc"],j["maxiter"],j["skip"],j["oslimit"],entry_id, j["summarylog"], j["initII"]))
      entry_id = entry_id+1


