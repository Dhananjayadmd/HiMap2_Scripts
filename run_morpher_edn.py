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

def main(no_clusters, no_init,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c, arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id,summary_log,initII):

  HIMAP2_HOME = '/home/dmd/Workplace/HiMap2'	
  #if not 'HIMAP2_HOME' in os.environ:
    #raise Exception('Set HIMAP2_HOME directory as an environment variable (Ex: export HIMAP2_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

  #HIMAP2_HOME = os.getenv('HIMAP2_HOME')
  DFG_GEN_HOME = HIMAP2_HOME + '/Morpher_DFG_Generator'
  DFG_CLUSTRNG_HOME = HIMAP2_HOME + '/HiMap2_Scikit_Clustering'
  MAPPER_HOME = HIMAP2_HOME + '/Morpher_CGRA_Mapper'
  #SIMULATOR_HOME = HIMAP2_HOME + '/hycube_simulator'

  dir_name = 'Entry_%s_Clusters_%s_Init_%s_C1_%s_C2_%s_r_%s_c_%s_arch_%s_maxIter_%s_skip_%s_oslimit_%s/' % (entry_id,no_clusters, no_init,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c, arch_desc, maxIter,skip_inter_or_intra, open_set_limit)
  sum_log_name = '_entry_%s_clusters_%s_Init_%s_C1_%s_C2_%s_r_%s_c_%s_arch_%s_maxIter_%s_skip_%s_oslimit_%s' % (entry_id,no_clusters, no_init,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c, arch_desc, maxIter,skip_inter_or_intra, open_set_limit)

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/edn/'
  DFG_CLUSTRNG_KERNEL = DFG_CLUSTRNG_HOME + '/applications/edn/' + dir_name
  MAPPER_KERNEL = MAPPER_HOME + '/applications/clustered_arch/edn/'+ dir_name
  EXECTIME_SUMMARY = HIMAP2_HOME + '/HiMap2_Scripts/exec_time/edn/' 
  #SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(DFG_CLUSTRNG_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(EXECTIME_SUMMARY)

  #dir_path = os.path.join(KERNEL_HOME, dir_name)
  #print('Changing directory to %s' % dfg_path)
  #if not os.path.isdir(dfg_path):
  #	os.makedirs(dfg_path)
  sum_file_name = EXECTIME_SUMMARY+'summary'+sum_log_name+'.log'
   
     
  
  f=open(sum_file_name, "a+")
  f.write("\n**********************************\n")
  f.write("Clustering: \n Number of Clusters: %s\n Init: %s\n C1: %s\n C2: %s\n CGRA r: %s\n CGRA c: %s \n\nCGRA Mapping: \n Architecture: %s\n MaxIter: %s\n Skip Intra or inter %s\n Open set limit: %s" % (no_clusters, no_init,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c, arch_desc, maxIter,skip_inter_or_intra, open_set_limit))




##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  #os.system('./run_pass.sh jpegdct')
  os.system('dot -Tpdf jpegdct_POST_LN111_PartPredDFG.dot -o jpegdct_POST_LN111_PartPredDFG.pdf')
  os.system('cp jpegdct_POST_LN111_PartPred_DFG_forclustering.xml '+DFG_CLUSTRNG_KERNEL)
  os.system('cp jpegdct_POST_LN111_PartPred_DFG.xml '+ MAPPER_KERNEL)

  print('\nRunning DFG Clustering\n')
  os.chdir(DFG_CLUSTRNG_KERNEL)
  os.system('python ../../../dfg_clustering.py jpegdct_POST_LN111_PartPred_DFG_forclustering.xml %s %s %s > log1.txt' % (no_clusters, ('precomputed'), no_init))
  os.system('dot -Tpdf inter_cluster.dot -o inter_cluster_graph_edn_%s_%s.pdf' % (no_clusters, no_init))
  os.system('cp clustered.png clustered_%s_%s.png' % (no_clusters, no_init))
	
  os.system('cp clustering_outcome.txt '+ MAPPER_KERNEL)
  os.system('cp inter_cluster_edges.txt '+ MAPPER_KERNEL)
  
  print('\nRunning modified SPKM cluster mapping\n')
  os.system('python ../../../cluster_level_mapping_spkmModified.py %s %s %s %s > log2.txt' % (C1_init_,C2_init_,cgra_cluster_r,cgra_cluster_c))
  os.system('cp dfg_to_cgra_cluster_mapping_outcome.txt '+ MAPPER_KERNEL)





##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)
  start = time.time()

  os.system(HIMAP2_HOME+'/Morpher_CGRA_Mapper/build_hierarchical/src/cgra_xml_mapper -m %s -d jpegdct_POST_LN111_PartPred_DFG.xml -j %s -s %s -l %s -u %s -a %s -i %s > log.txt &' % (maxIter,HIMAP2_HOME+'/Morpher_CGRA_Mapper/json_arch/clustered_archs/'+arch_desc, skip_inter_or_intra, open_set_limit,HIMAP2_HOME+'/HiMap2_Scripts/'+summary_log, entry_id, initII))
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
    no_clusters = sys.argv[1]
    no_init = sys.argv[2]    
    C1_init = sys.argv[3]
    C2_init = sys.argv[4]
    cgra_cluster_r = sys.argv[5]
    cgra_cluster_c = sys.argv[6]
    arch_desc = sys.argv[7]
    maxIter = sys.argv[8]
    skip_inter_or_intra = sys.argv[9]    
    open_set_limit = sys.argv[10]  
    entry_id = sys.argv[11]
    summary_log = sys.argv[12]
    initII = sys.argv[13]
    main(no_clusters, no_init,C1_init, C2_init,cgra_cluster_r, cgra_cluster_c,arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id,summary_log, initII)
