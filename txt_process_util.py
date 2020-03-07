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
	
  
    

    