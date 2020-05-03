from groupTxt_ByClass import groupItemsBySingleKeyIndex
from nltk.stem import PorterStemmer 

def extractSeenNotClustered(predsSeen_list_pred_true_words_index, sub_list_pred_true_words_index):
  not_clustered_inds_batch=[]
  
  predSeenIndex=[]
  for item in predsSeen_list_pred_true_words_index:
    predSeenIndex.append(item[3])

  for item in sub_list_pred_true_words_index:
    index = item[3]
    if index in predSeenIndex:
      continue
    not_clustered_inds_batch.append([item[0], item[1], item[2], item[3], item[4]])	  
  
  return not_clustered_inds_batch

def print_by_group(listtuple_pred_true_text, grIndex):
  dic_tupple_class=groupItemsBySingleKeyIndex(listtuple_pred_true_text, grIndex)
  for label, pred_true_txts in sorted(dic_tupple_class.items()):
    Print_list_pred_true_text(pred_true_txts)
  print("total groups=", len(dic_tupple_class))	
  
def Print_list_pred_true_text(listtuple_pred_true_text):
  for pred_true_text in listtuple_pred_true_text:
    print(pred_true_text)

def readlistWholeJsonDataSet(datasetName):
  ps = PorterStemmer()
  file1=open(datasetName,"r")
  lines = file1.readlines()
  file1.close()
  list_pred_true_words_index_lockindex=[]
  i=-1  
  for line in lines:
    line=line.strip()  
    n = eval(line)
    id=str(n['Id']).strip()  
    true=str(n['clusterNo']).strip()
    words=str(n['textCleaned']).strip().split(' ')
    if len(true)==0 or len(words)==0:
      continue
    i+=1
    words=[ps.stem(w) for w in words] 	
    list_pred_true_words_index_lockindex.append([-1, true, words, i, i])
  return list_pred_true_words_index_lockindex
  
def readDicWholeJsonDataSet(datasetName):
  ps = PorterStemmer() 
  file1=open(datasetName,"r")
  lines = file1.readlines()
  file1.close()
  dic_id_trueWords={}
  for line in lines:
    line=line.strip()  
    n = eval(line)
    id=str(n['Id']).strip()  
    true=str(n['clusterNo']).strip()
    words=str(n['textCleaned']).strip().split(' ')
    if len(true)==0 or len(words)==0:
      continue
    words=[ps.stem(w) for w in words] 		  
    dic_id_trueWords[id]=[true, words]
  return dic_id_trueWords
  

  