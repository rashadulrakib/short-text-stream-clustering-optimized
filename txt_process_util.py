from collections import Counter
from compute_util import computeTextSimCommonWord_WordDic
from scipy.spatial.distance import cosine

def commonWordSims_clusterGroup(word_arr, dic_ClusterGroups):
  dic_lex_Sim_CommonWords={}
  maxPredLabel_lex=''
  maxSim_lex=-1000000
  maxCommon_lex=-100000
  minSim_lex=10000000000  
  for label, dicWords_totalWCount in dic_ClusterGroups.items():
    #listWord_arr=extractBySingleIndex(pred_true_txt_ind_prevPredss, 2)
    #merged = list(itertools.chain.from_iterable(listWord_arr))	
    #comText=combineDocsToSingle(listStrs)

    dic_words_i=Counter(word_arr)
    totalWCount_i=len(word_arr)	
    dic_words_j=dicWords_totalWCount[0]
    totalWCount_j=dicWords_totalWCount[1]
    txtSim, commonCount=computeTextSimCommonWord_WordDic(dic_words_i, dic_words_j, totalWCount_i, totalWCount_j)

    	
    str_label=str(label)	
    #txtSim, commonCount=computeTextSimCommonWord_WordArr(word_arr, merged)
    dic_lex_Sim_CommonWords[str_label]=[txtSim, commonCount]
    if maxSim_lex<txtSim:
      maxSim_lex=txtSim
      maxPredLabel_lex=str_label
      maxCommon_lex=commonCount	  
    if minSim_lex>txtSim:
        minSim_lex=txtSim	
     
  return [dic_lex_Sim_CommonWords, maxPredLabel_lex, maxSim_lex, maxCommon_lex, minSim_lex]


def commonWordSims(word_arr, dic_itemGroups):
  dic_lex_Sim_CommonWords={}
  for label, pred_true_txt_ind_prevPredss in dic_itemGroups.items():
    listWord_arr=extractBySingleIndex(pred_true_txt_ind_prevPredss, 2)
    merged = list(itertools.chain.from_iterable(listWord_arr))	
    #comText=combineDocsToSingle(listStrs)
    txtSim, commonCount=computeTextSimCommonWord_WordArr(word_arr, merged)
    dic_lex_Sim_CommonWords[str(label)]=[txtSim, commonCount]	
     
  return dic_lex_Sim_CommonWords  

def semanticSims(text_Vec, dic_centerVecs):
  dic_semanticSims={}
  maxPredLabel_Semantic=''
  maxSim_Semantic=-1000
  minSim_semantic=1000000000
  
  for label, centVec in dic_centerVecs.items():
    str_label=str(label)

    sim = 1-cosine(centVec, text_Vec)
    dic_semanticSims[str_label]=sim
    if maxSim_Semantic<sim:
      maxSim_Semantic=sim
      maxPredLabel_Semantic=str_label
    if minSim_semantic>sim:
        minSim_semantic=sim	

  return [dic_semanticSims, maxPredLabel_Semantic, maxSim_Semantic, minSim_semantic]  

def concatWordsSort(words):
  words.sort()
  combinedWord=' '.join(words)
  return combinedWord  

def createBinaryWordCooccurenceMatrix(listtuple_pred_true_text_ind):
  binGraph=[]
  uniqueWordList=set()  
  docWords=[]  
  for i in range(len(listtuple_pred_true_text_ind)):
    words=listtuple_pred_true_text_ind[i][2]
    uniqueWordList.update(words)
    docWords.append(words)
  
  dic_word_index={}
  i=-1 
  for word in uniqueWordList:
    i=i+1
    dic_word_index[word]=i	
   	
  m=len(uniqueWordList)	
  binGraph = [[0] * m for i in range(m)]
  for words in docWords:
    for i in range(1,len(words)):	  
      id1=dic_word_index[words[i-1]]
      id2=dic_word_index[words[i]]
      binGraph[id1][id2]=1 	      	  
   
  return [binGraph, dic_word_index, docWords]

def createTerm_Doc_matrix_dic(dic_bitri_keys_selectedClusters_seenBatch):
  term_doc_matrix=[] #n by m matrix
  
  unique_txtIds=[]
  
  for key, txtInds in dic_bitri_keys_selectedClusters_seenBatch.items():
    unique_txtIds=unique_txtIds+txtInds
  
  unique_txtIds=set(unique_txtIds)
  
  n = len(dic_bitri_keys_selectedClusters_seenBatch)
  m = len(unique_txtIds)
  term_doc_matrix = [[0] * m for i in range(n)]
  print("unique_txtIds", len(unique_txtIds))
  dic_txt_index={}
  i=-1  
  for txtInd in unique_txtIds:
    i+=1
    dic_txt_index[txtInd]=i

  rowId=-1 	
  for key, txtInds in dic_bitri_keys_selectedClusters_seenBatch.items():
    rowId+=1          
    for txtInd in txtInds:
     colId=dic_txt_index[txtInd]
     term_doc_matrix[rowId][colId]=1

  #print(term_doc_matrix)
  return [term_doc_matrix, dic_txt_index]	 
	
  
    

    