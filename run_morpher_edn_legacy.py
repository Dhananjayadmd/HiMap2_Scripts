  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
import time 
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

def main(arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id):

  HIMAP2_HOME = '/home/dmd/Workplace/HiMap2'	
  #if not 'HIMAP2_HOME' in os.environ:
    #raise Exception('Set HIMAP2_HOME directory as an environment variable (Ex: export HIMAP2_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

  #HIMAP2_HOME = os.getenv('HIMAP2_HOME')
  DFG_GEN_HOME = HIMAP2_HOME + '/Morpher_DFG_Generator'
  DFG_CLUSTRNG_HOME = HIMAP2_HOME + '/HiMap2_Scikit_Clustering'
  MAPPER_HOME = HIMAP2_HOME + '/Morpher_CGRA_Mapper'
  #SIMULATOR_HOME = HIMAP2_HOME + '/hycube_simulator'

  dir_name = 'Legacy_Entry_%s_s_arch_%s_maxIter_%s_skip_%s_oslimit_%s/' % (entry_id, arch_desc, maxIter,skip_inter_or_intra, open_set_limit)
  sum_log_name = '_legacy_entry_%s_arch_%s_maxIter_%s_skip_%s_oslimit_%s' % (entry_id, arch_desc, maxIter,skip_inter_or_intra, open_set_limit)

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/edn/'
  #DFG_CLUSTRNG_KERNEL = DFG_CLUSTRNG_HOME + '/applications/edn/' + dir_name
  MAPPER_KERNEL = MAPPER_HOME + '/applications/clustered_arch/edn/'+ dir_name
  EXECTIME_SUMMARY = HIMAP2_HOME + '/HiMap2_Scripts/exec_time/edn/' 
  #SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/'

  my_mkdir(DFG_GEN_KERNEL)
  #my_mkdir(DFG_CLUSTRNG_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(EXECTIME_SUMMARY)

  #dir_path = os.path.join(KERNEL_HOME, dir_name)
  #print('Changing directory to %s' % dfg_path)
  #if not os.path.isdir(dfg_path):
  #	os.makedirs(dfg_path)
  sum_file_name = EXECTIME_SUMMARY+'summary'+sum_log_name+'.log'
   
     
  
  f=open(sum_file_name, "a+")
  f.write("\n**********************************\n")
  f.write("CGRA Mapping: \n Architecture: %s\n MaxIter: %s\n Skip Intra or inter %s\n Open set limit: %s" % (arch_desc, maxIter,skip_inter_or_intra, open_set_limit))




##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  #os.system('./run_pass.sh jpegdct')
  os.system('dot -Tpdf jpegdct_POST_LN111_PartPredDFG.dot -o jpegdct_POST_LN111_PartPredDFG.pdf')
  #os.system('cp jpegdct_POST_LN111_PartPred_DFG_forclustering.xml '+DFG_CLUSTRNG_KERNEL)
  os.system('cp jpegdct_POST_LN111_PartPred_DFG.xml '+ MAPPER_KERNEL)








##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)
  start = time.time()

  os.system(HIMAP2_HOME+'/Morpher_CGRA_Mapper/build_legacy/src/cgra_xml_mapper -m %s -d jpegdct_POST_LN111_PartPred_DFG.xml -j %s -s %s -l %s > log.txt &' % (maxIter,HIMAP2_HOME+'/Morpher_CGRA_Mapper/json_arch/clustered_archs/'+arch_desc, skip_inter_or_intra, open_set_limit))
  os.system('neato -Tpdf arch_allconnections.dot -o %s.pdf' % (arch_desc))
  os.system('neato -Tpdf arch_interclusterconnections.dot -o %s_interclusterconnections.pdf' % (arch_desc))

  end = time.time() 

  f.write("\n\nExecution time: %s"% (end - start))   
  f.close() 


def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    arch_desc = sys.argv[1]
    maxIter = sys.argv[2]
    skip_inter_or_intra = sys.argv[3]    
    open_set_limit = sys.argv[4]  
    entry_id = sys.argv[5]
    main(arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id)
