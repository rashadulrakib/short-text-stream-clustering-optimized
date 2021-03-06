from collections import Counter

def evaluateByGram(dic_gramkeys_txtInds, seen_list_pred_true_words_index_lockindex):
  texts_clustered_sum=0
  max_group_sum=0
  #bigger_clusters_tri=0
  #bigger_clusters_bi=0
  predsseen_list_pred_true_words_index_lockindex_lockindex=[]  
  unique_txtIds=[]  
  
  temp_txtId_to_pred={}
  
  for mergedKey, txtInds in dic_gramkeys_txtInds.items():
    txtInds=list(set(txtInds)) 
    texts_clustered_sum+=len(txtInds)
    unique_txtIds=unique_txtIds+txtInds	
    #if len(txtInds)>1: bigger_clusters_tri+=1  
    print("evaluateByGram",mergedKey, txtInds)   
    true_label_list=[]
    for txtInd in txtInds:
      
	  #temp , may be useful
      temp_txtId_to_pred.setdefault(txtInd, []).append(mergedKey)
      if len(temp_txtId_to_pred[txtInd])>1:
        print("batch-eval, temp_txtId_to_pred=", txtInd, temp_txtId_to_pred[txtInd])
        continue
      #temp  		
	  
      true_label_list.append(seen_list_pred_true_words_index_lockindex[txtInd][1])
	  
      predsseen_list_pred_true_words_index_lockindex_lockindex.append([mergedKey,seen_list_pred_true_words_index_lockindex[txtInd][1],seen_list_pred_true_words_index_lockindex[txtInd][2],seen_list_pred_true_words_index_lockindex[txtInd][3], seen_list_pred_true_words_index_lockindex[txtInd][4]])
	  
    max_group_sum+=max(Counter(true_label_list).values())
    #print("true_label_list", len(true_label_list), true_label_list)
	

  	
  	
  
  print("batch-eval", max_group_sum, texts_clustered_sum, "accuracy", max_group_sum/texts_clustered_sum, "#clusters", len(dic_gramkeys_txtInds), '#unique_txtIds', len(set(unique_txtIds)))
  return predsseen_list_pred_true_words_index_lockindex_lockindex