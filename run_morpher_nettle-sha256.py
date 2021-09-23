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

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/nettle-sha256/'
  DFG_CLUSTRNG_KERNEL = DFG_CLUSTRNG_HOME + '/applications/nettle-sha256/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/clustered_arch/nettle-sha256/'
  #SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/array_add/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(DFG_CLUSTRNG_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  #my_mkdir(SIMULATOR_KERNEL)



##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  #os.system('./run_pass.sh _nettle_sha256_compress')
  os.system('dot -Tpdf _nettle_sha256_compress_INNERMOST_LN1_PartPredDFG.dot -o _nettle_sha256_compress_INNERMOST_LN1_PartPredDFG.pdf')
  os.system('cp _nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG_forclustering.xml '+DFG_CLUSTRNG_KERNEL)
  os.system('cp _nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG.xml '+ MAPPER_KERNEL)

  print('\nRunning DFG Clustering\n')
  os.chdir(DFG_CLUSTRNG_KERNEL)
  #os.system('python ../../dfg_clustering.py _nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG_forclustering.xml 8 %s 100' % ("precomputed"))
  os.system('dot -Tpdf inter_cluster.dot -o inter_cluster_graph_nettle_sha256.pdf')
  os.system('dot -Tpng inter_cluster.dot -o inter_cluster_graph_nettle_sha256.png')
  os.system('cp clustering_outcome.txt '+ MAPPER_KERNEL)
  os.system('cp inter_cluster_edges.txt '+ MAPPER_KERNEL)
  
  print('\nRunning modified SPKM cluster mapping\n')
  #os.system('python ../../cluster_level_mapping_spkmModified.py 2 2 3 3')
  os.system('cp dfg_to_cgra_cluster_mapping_outcome.txt '+ MAPPER_KERNEL)



##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system(HIMAP2_HOME+'/Morpher_CGRA_Mapper/build/src/cgra_xml_mapper  -d _nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG.xml -j '+HIMAP2_HOME+'/Morpher_CGRA_Mapper/json_arch/clustered_archs/stdnoc_3x3tiles_3x3PEs.json')
  os.system('dot -Tpdf %s -o %s' % ('rec_cycles_colored.dot','rec_cycles_colored.pdf'))
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
