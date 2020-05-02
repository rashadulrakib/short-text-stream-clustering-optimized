from general_util import readlistWholeJsonDataSet
from general_util import extractSeenNotClustered
from general_util import print_by_group
from clustering_sd import cluster_sd
from clustering_gram import cluster_gram_freq
from collections import Counter
from clustering_gram_util import filterClusters
from clustering_gram_util import assignToClusterBySimilarity
from clustering_gram_util import assignToClusterSimDistribution
from evaluation_util import evaluateByGram
from dictionary_util import combineTwoDictionary
from word_vec_extractor import extractAllWordVecs
from print_cluster_evaluation import appendResultFile
import os
from evaluation import Evaluate
from read_pred_true_text import ReadPredTrueText

from datetime import datetime

gloveFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/glove.42B.300d/glove.42B.300d.txt"
wordVectorsDic={}
#wordVectorsDic = extractAllWordVecs(gloveFile, 300)

list_pred_true_words_index_lockindex=readlistWholeJsonDataSet("Tweets") #NTS-mstream, #Tweets, #News
fileName="News_clusters"
fileName_to_assigned="News_clusters_to-assign"

if os.path.exists(fileName):
  os.remove(fileName)
if os.path.exists(fileName_to_assigned):
  os.remove(fileName_to_assigned)  
  
  
def populateNewList(globalList_not_clustered):
  list_pred_true_words_index_lockindex=[]
  for i in range(len(globalList_not_clustered)):
    item=globalList_not_clustered[i]
    list_pred_true_words_index_lockindex.append([item[0], item[1], item[2], i, item[4]])

  return list_pred_true_words_index_lockindex	
  

def clusterByBatch(batchSize, list_pred_true_words_index_lockindex, simThreshold=0.1, minCommomGram=2):
  allTexts=len(list_pred_true_words_index_lockindex)
  batchNo=0
  dic_bitri_keys_selectedClusters_seenBatch={}
  
  globalList_clustered=[]
  globalList_not_clustered=[]

  for start in range(0,allTexts,batchSize): 
    batchNo+=1
    end= start+batchSize if start+batchSize<allTexts else allTexts  
    print(start, end)
    sub_list_pred_true_words_index_lockindex=list_pred_true_words_index_lockindex[start:end]
    print(len(sub_list_pred_true_words_index_lockindex))
    #cluster_sd(sub_list_pred_true_words_index_lockindex)
  
    dic_bitri_keys_selectedClusters_seenBatch=cluster_gram_freq(simThreshold, minCommomGram, sub_list_pred_true_words_index_lockindex, batchNo, dic_bitri_keys_selectedClusters_seenBatch,  list_pred_true_words_index_lockindex[0:end])
  
    predsSeen_list_pred_true_words_index_lockindex=evaluateByGram(dic_bitri_keys_selectedClusters_seenBatch, list_pred_true_words_index_lockindex[0:end])
    not_clustered_inds_batch=extractSeenNotClustered(predsSeen_list_pred_true_words_index_lockindex, sub_list_pred_true_words_index_lockindex)
  
    #not_clustered_inds_seen_batch.extend(not_clustered_inds_batch)
  
    #not_clustered_inds_batch=assignToClusterSimDistribution(not_clustered_inds_batch, dic_bitri_keys_selectedClusters_seenBatch, list_pred_true_words_index_lockindex[0:end], wordVectorsDic)
    globalList_clustered.extend(predsSeen_list_pred_true_words_index_lockindex)
    globalList_not_clustered.extend(not_clustered_inds_batch)
  
  
    #Evaluate(predsSeen_list_pred_true_words_index_lockindex) #+not_clustered_inds_batch) 
    print("total texts=", len(predsSeen_list_pred_true_words_index_lockindex))
	

  print("--------evaluate global gram clustering-------")		
  temp_list=[]
  temp_dic_txtInd={}
  for item in globalList_clustered:
    ind=item[3]
    if ind in temp_dic_txtInd:
      continue
    temp_list.append([item[0], item[1], item[2], item[3], item[4]])	
    temp_dic_txtInd[ind]=item		
        
  globalList_clustered=temp_list		
  Evaluate(globalList_clustered)
	
  #update list_pred_true_words_index_lockindex
  #update batchSize each time we call clusterByBatch  
  print("total texts=", len(globalList_clustered+globalList_not_clustered))
  return [globalList_clustered, globalList_not_clustered]


all_global=[]

now = datetime.now()

globalList_clustered, globalList_not_clustered=clusterByBatch(4000, list_pred_true_words_index_lockindex,0.08, 2)
all_global.extend(globalList_clustered)

list_pred_true_words_index_lockindex=populateNewList(globalList_not_clustered)
globalList_clustered, globalList_not_clustered=clusterByBatch(4000, list_pred_true_words_index_lockindex, 0.08, 2)
all_global.extend(globalList_clustered)

list_pred_true_words_index_lockindex=populateNewList(globalList_not_clustered)
globalList_clustered, globalList_not_clustered=clusterByBatch(4000, list_pred_true_words_index_lockindex, 0.08, 2)
all_global.extend(globalList_clustered)








Evaluate(all_global)
print("final total texts=", len(all_global+globalList_not_clustered))

later = datetime.now()
difference = (later - now).total_seconds()  
print("time diff", difference)	


