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

list_pred_true_words_index=readlistWholeJsonDataSet("Tweets") #NTS-mstream, #Tweets, #News
fileName="News_clusters"
fileName_to_assigned="News_clusters_to-assign"

if os.path.exists(fileName):
  os.remove(fileName)
if os.path.exists(fileName_to_assigned):
  os.remove(fileName_to_assigned)  





allTexts=len(list_pred_true_words_index)
batchSize=4000

batchNo=0

dic_bitri_keys_selectedClusters_seenBatch={}
#not_clustered_inds_seen_batch=[]

now = datetime.now()

globalList_clustered=[]
globalList_not_clustered=[]

for start in range(0,allTexts,batchSize): 
  batchNo+=1
  end= start+batchSize if start+batchSize<allTexts else allTexts  
  print(start, end)
  sub_list_pred_true_words_index=list_pred_true_words_index[start:end]
  print(len(sub_list_pred_true_words_index))
  #cluster_sd(sub_list_pred_true_words_index)
  
  dic_bitri_keys_selectedClusters_seenBatch=cluster_gram_freq(sub_list_pred_true_words_index, batchNo, dic_bitri_keys_selectedClusters_seenBatch,  list_pred_true_words_index[0:end])
  
  predsSeen_list_pred_true_words_index=evaluateByGram(dic_bitri_keys_selectedClusters_seenBatch, list_pred_true_words_index[0:end])
  not_clustered_inds_batch=extractSeenNotClustered(predsSeen_list_pred_true_words_index, sub_list_pred_true_words_index)
  
  #not_clustered_inds_seen_batch.extend(not_clustered_inds_batch)
  
  #not_clustered_inds_batch=assignToClusterSimDistribution(not_clustered_inds_batch, dic_bitri_keys_selectedClusters_seenBatch, list_pred_true_words_index[0:end], wordVectorsDic)
  globalList_clustered.extend(predsSeen_list_pred_true_words_index)
  globalList_not_clustered.extend(not_clustered_inds_batch)
  
  
  Evaluate(predsSeen_list_pred_true_words_index) #+not_clustered_inds_batch) 
  print("total texts=", len(predsSeen_list_pred_true_words_index)+len(not_clustered_inds_batch))
  
  
  
  #texts in cluster + texts not in cluster should be =2000
  '''dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch, dic_combined_keys_selectedClusters, new_sub_list_pred_true_words_index=filterClusters(dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, sub_list_pred_true_words_index, list_pred_true_words_index[0:end])
  
  not_clustered_inds_seen_batch.extend(not_clustered_inds_currentBatch)
  
  appendResultFile(new_sub_list_pred_true_words_index, fileName)
  
  if batchNo>=1: # and batchNo%2==0:
    dic_preds, new_not_clustered_inds_seen_batch=assignToClusterBySimilarity(not_clustered_inds_seen_batch, list_pred_true_words_index[0:end], dic_combined_keys_selectedClusters, wordVectorsDic)
	
    #appendResultFile(new_not_clustered_inds_seen_batch, fileName)
    appendResultFile(new_not_clustered_inds_seen_batch, fileName_to_assigned)	
    	
	
    #new_comb=combineTwoDictionary(dic_preds,dic_combined_keys_selectedClusters, False)	
    #evaluateByGram(new_comb, list_pred_true_words_index[0:end])	
    not_clustered_inds_seen_batch=[]'''

'''listtuple_pred_true_text=ReadPredTrueText(fileName)
Evaluate(listtuple_pred_true_text)'''	

print('----------global list-----------')
Evaluate(globalList_clustered)      
	  
later = datetime.now()
difference = (later - now).total_seconds()  
print("time diff", difference)


print("--------evaluate global gram clustering-------")		
temp_list=[]
temp_dic_txtInd={}
for item in globalList_clustered:
  ind=item[3]
  if ind in temp_dic_txtInd:
    continue
  temp_list.append([item[0], item[1], item[2], item[3]])	
  temp_dic_txtInd[ind]=item		
        
globalList_clustered=temp_list		
Evaluate(globalList_clustered)
print('------print_by_group(globalList_clustered, 0)----')
print_by_group(globalList_clustered, 0)
print('------print_by_group(globalList_not_clustered, 0)----')
print_by_group(globalList_not_clustered, 1)
print("final==", len(globalList_clustered)+len(globalList_not_clustered))