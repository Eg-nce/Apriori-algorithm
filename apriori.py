from itertools import combinations 
from collections import defaultdict
import pandas as pd
import itertools
import math
import numpy as np


class apriori:
  def __init__(self,Data, Minsup , Confidence):
    self.data = Data
  
    self.minsup = int(math.ceil((Minsup*len(self.data.values.tolist()))/100))
    self.Main_dic = None
    self.confidence_rate = float(Confidence/100)
  
  def __data_pre(self):
     s1 ={}
     self.pre_data = self.data
     CleanData = []
     try:
           self.data =  self.data.applymap(str.lower)
     except:
            TypeError
     self.pre_data =  self.pre_data.fillna('NaNxx')
     self.pre_data = self.pre_data.values.tolist()
     i = 0 
     while True:
          try:
              self.pre_data[i].remove("NaNxx")
          except :   
             ValueError
             i = i + 1 
          if i == len(self.pre_data):
            break  
     
     for i in self.pre_data:
        for j in i:
            if j in s1:
                s1[j] += 1
            else:
                s1[j] = 1
     for x , y in s1.items():
         if y < self.minsup:
           for elements in self.pre_data:
              if x  in elements:
                elements.remove(x)
      
     return self.pre_data ,s1
  
  def __unique(self):
    liste , single = self.__data_pre() 
    Unique_set = set()
    for lis in liste :
       for item in lis:
         Unique_set.add(item)
    unique =  list(Unique_set)   
    return unique
  
  def __ItemDatas(self):
      unique_list = self.__unique()
      search  = []
      cmb = 0
      cmb = 1 
      dic = dict()
      for gt in range(len(unique_list)):
          comb = ()
          cmb = cmb +1
          comb = combinations(unique_list,cmb )      
          for i in comb:
              G = []
              G.append(i)
              out = [item for t in G for item in t]
              search.append(out)
      for x in search: 
          dic.update({tuple(sorted(x)):0})
       
      self.Main_dic = dic  
      return  self.Main_dic
 
  def __sorter(self):
    candicates = []
    dic  = self.__ItemDatas()
  
    for x in dic.keys():
      candicates.append(sorted(list(x)))
    
    return  candicates 



  def __Counter(self):
    data , single = self.__data_pre() 
    candicates  = self.__sorter()
    dic = self.__ItemDatas()
    deneme = []
    s1 = 0
    s2 = 0

    while True:
      item = set(sorted(candicates[s1]))
      target = set(sorted(data[s2]))
      if item.issubset(target) == True:
          
            dic[tuple(sorted(item))] += 1 
            s1 = s1 + 1 
      else:
        s1 = s1 + 1    
       
      if s1 == len(candicates):
       
       s2 +=1
       s1 = 0
     
      if s2 == len(data):
         break
        
    return  dic 


  
  def __Minsup_Terminator(self):
    data, single = self.__data_pre()
    dicni  = self.__Counter()
    Terminated_list = []
    s1 = {}
    for  gtx,rtx in dicni.items():
       if rtx >= self.minsup:
          s1.update({gtx : rtx})

    return s1 
   
  def __confidence(self):
    data, single = self.__data_pre()
    set_list = []
    minsup_list = self.__Minsup_Terminator()
    j = 0
    i = 0
    confidence_list = []
    if len(minsup_list) == 0 :
      return print("minumum supports and confidences does not exist !!!\n try decrease minsup or confidence rate")


  
    for x in minsup_list.keys():
      set_list.append(set(x))
    while True:
      confidence = []
      for x in single.keys():
          f = set(((x),))
          if f.issubset(set_list[j]):
            single_min = single.get(x)
            main_min = minsup_list.get(tuple(sorted(set_list[j])))
            rate = float(main_min/single_min)
            if rate >= self.confidence_rate:
              k = list(set_list[j])
              confidence = [x ,'=============>', k, "confidence = %{}".format("%.2f" % (rate*100))  ]
              confidence_list.append(confidence)
      j = j + 1
      if j == len(set_list):
    
        break
      
      h = 0
      i = 1 

      while True:
        if set_list[h].issubset(set_list[i]):
          target_min = minsup_list.get(tuple(sorted(set_list[h])))
          Big_min = minsup_list.get(tuple(sorted(set_list[i])))
          rate_1 = float(Big_min/target_min)
          
          
          if rate_1 >= self.confidence_rate:
              
              confidence1 = [list(set_list[h]) ,'=============>',  list(set_list[i]) ,"confidence = %{}".format("%.2f" %( rate_1*100)) ]
              confidence_list.append(confidence1)
          h = h +1
          i = h +1
        
        else:
          i = i +1 
          
        if i == len(set_list):
            h = h +1 
            i = h  +1
        if h == len(set_list)-1:
          break    
   
        
    return confidence_list
            
  

   
  def Miner(self):
    minsup_list = self.__Minsup_Terminator()
    liste , single = self.__data_pre() 
    if len(minsup_list) == 0 :
       raise TypeError("minimum support candidate and confidences does not exist !!!\n try decrease minsup or confidence rate")
      
    Confidence_List = self.__confidence()
    Single_Minsup = [tuple(((x,))) for x in single.keys()]
    Single_Minsup_Values = [ _ for _ in single.values()]
    
    Multi_Minsup = list(map(tuple,minsup_list))
    Multi_Minsup_Values = [ _ for _ in minsup_list.values()]
    var = 0
    var2 = 0
    Frequency_list = []
    while True:
        Frequency_item = [Multi_Minsup[var] , 'frequency ===> %{}'.format("%.2f" %  ((Multi_Minsup_Values[var] * 100 )/len(self.data))) ]
        Frequency_list.append(Frequency_item)
        var +=1
        if var == len(Multi_Minsup_Values):
          while True:
            if Single_Minsup_Values[var2] >= self.minsup:
              Frequency_item = [  Single_Minsup[var2] , 'frequency ===> %{}'.format("%.2f" %  ((Single_Minsup_Values[var2] * 100 )/len(self.data))) ]
              Frequency_list.append(Frequency_item)
              var2 +=1
            else:
               var2 +=1  
            if var2 == len(Single_Minsup_Values):
                break     
          break 
    return Frequency_list , Confidence_List



         

