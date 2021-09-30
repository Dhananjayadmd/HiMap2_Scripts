  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

def main():

  HIMAP2_HOME = '/home/dmd/Workplace/HiMap2'	
  #if not 'HIMAP2_HOME' in os.environ:
    #raise Exception('Set HIMAP2_HOME directory as an environment variable (Ex: export HIMAP2_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

  #HIMAP2_HOME = os.getenv('HIMAP2_HOME')
  DFG_GEN_HOME = HIMAP2_HOME + '/Morpher_DFG_Generator'
  DFG_CLUSTRNG_HOME = HIMAP2_HOME + '/HiMap2_Scikit_Clustering'
  MAPPER_HOME = HIMAP2_HOME + '/Morpher_CGRA_Mapper'
  #SIMULATOR_HOME = HIMAP2_HOME + '/hycube_simulator'

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/edn/'
  DFG_CLUSTRNG_KERNEL = DFG_CLUSTRNG_HOME + '/applications/edn/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/clustered_arch/edn/'
  #SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/array_add/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(DFG_CLUSTRNG_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  #my_mkdir(SIMULATOR_KERNEL)



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
  #os.system('python ../../dfg_clustering.py jpegdct_POST_LN111_PartPred_DFG_forclustering.xml 7 %s 100' % ('precomputed'))
  os.system('dot -Tpdf inter_cluster.dot -o inter_cluster_graph_edn_7_100.pdf')
  os.system('cp clustered.png clustered_7_100.png')
	
  #os.system('python ../../dfg_clustering.py jpegdct_POST_LN111_PartPred_DFG_forclustering.xml 10 %s 100' % ('precomputed'))
  #os.system('dot -Tpdf inter_cluster.dot -o inter_cluster_graph_edn_10_100.pdf')
  #os.system('cp clustered.png clustered_10_100.png')
  os.system('cp clustering_outcome.txt '+ MAPPER_KERNEL)
  os.system('cp inter_cluster_edges.txt '+ MAPPER_KERNEL)
  
  print('\nRunning modified SPKM cluster mapping\n')
  #os.system('python ../../cluster_level_mapping_spkmModified.py 2 2 3 3')
  os.system('cp dfg_to_cgra_cluster_mapping_outcome.txt '+ MAPPER_KERNEL)





##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system(HIMAP2_HOME+'/Morpher_CGRA_Mapper/build/src/cgra_xml_mapper -m 60 -d jpegdct_POST_LN111_PartPred_DFG.xml -j '+HIMAP2_HOME+'/Morpher_CGRA_Mapper/json_arch/clustered_archs/stdnoc_3x3tiles_3x3PEs.json')
  os.system('neato -Tpdf %s -o %s' % ('arch_allconnections.dot','stdnoc_3x3tiles_4x4PEs.pdf'))
  os.system('neato -Tpdf %s -o %s' % ('arch_interclusterconnections.dot','stdnoc_3x3tiles_4x4PEs_interclusterconnections.pdf'))

  #os.system('../../../build/src/cgra_xml_mapper -d array_add_INNERMOST_LN1_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem.json -t HyCUBE_4REG')


def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
  main()
