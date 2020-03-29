from sent_vecgenerator import generate_sent_vecs_toktextdata
from scipy.spatial import distance
from scipy.spatial.distance import cosine
import sys


def computeTextSimCommonWord_WordDic(words_i, words_j, txt_i_len, txt_j_len):  
  text_sim=0
  commonCount=0
  
  len_i=len(words_i)
  len_j=len(words_j)

  if len_i>len_j:
    temp=words_i
    words_i=words_j
    words_j=temp    
 
  for word_i, i_count in words_i.items():
    if word_i in words_j.keys():
      commonCount=commonCount+i_count+words_j[word_i]
  
  if txt_i_len>0 and txt_j_len>0:
    text_sim=commonCount/(txt_i_len+txt_j_len)
    
  return [text_sim, commonCount]

def computeSimBtnList(txtIndsi, txtIndsj):
  if len(txtIndsj)<len(txtIndsi):
    temp=txtIndsj
    txtIndsj=txtIndsi
    txtIndsi=temp 

  common=0   
  for ind in txtIndsi:
    if ind in txtIndsj:
      common=common+1
	  
  return 2*common/(len(txtIndsi)+len(txtIndsj))	  
	  
	
  


def findCloseCluster_GramKey_lexical(keys_list, word_arr, minMatch):
  closeKey_Lexical=None
  maxCommonLength=0
  
  for key in keys_list:
    set1=set(key.split(' '))
    set2=set(word_arr)
    common=set1.intersection(set2)
    if len(common)>=minMatch and len(common)>maxCommonLength:
      maxCommonLength=len(common)	  
      closeKey_Lexical=key	  
  
  return closeKey_Lexical
  

def findCloseCluster_GramKey_Semantic(keys_list, word_arr, minMatch, wordVectorsDic, euclidean=True):
  closeKey_Semantic=None
  sent_vec=generate_sent_vecs_toktextdata([word_arr], wordVectorsDic, 300)[0]
  min_dist=sys.float_info.max
  max_sim=0  
  for key in keys_list:
    key_words=key.split(' ') 
    set1=set(key_words)
    set2=set(word_arr)
    common=set1.intersection(set2)	
    key_vec=generate_sent_vecs_toktextdata([key_words], wordVectorsDic, 300)[0]
    #eu_dist=0	
    #if euclidean==True:	
    #  eu_dist=distance.euclidean(sent_vec, key_vec)
    #else:
    eu_dist=cosine(sent_vec, key_vec) #cosine=distance
    sim=1-eu_dist	
    #if len(common)>=minMatch and min_dist>eu_dist:
    if len(common)>=minMatch and max_sim<sim: 	
      #min_dist=eu_dist
      max_sim=sim 	  
      closeKey_Semantic=key	  
    	
    	

  
  return [closeKey_Semantic, max_sim]  
  