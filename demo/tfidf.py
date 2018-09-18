# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import time

def gen_candidate_title(thr_tfidf_max = 10,thr_tfidf_min = 8 ,max_words_num = 20,num_candidate = 10,thr_tfidf = 8,path = os.path.join('.','pos'),path4testData = os.path.join('.','postxt')):    
    t_start = time.time()
    print("generate title ....")
    #========= build en2zh dictionary ==========================        
    #title_en2zh = {}            
    #title_zh2en = {}
    #test = {}
    #alltitle_path = r'C:\Users\順益\Desktop\106-NLP\final project'
        #tet = ''
        #tet.find('1+1')
        #tet[34354:34354+10]
    #with open(os.path.join(alltitle_path,'newAllTitle.txt'),'r',encoding = 'utf-8') as f:     
    #    for movie_title in f:
    #        en,zh = movie_title.split('\t')
    #        title_en2zh[en] = zh.strip('\n')
    #        title_zh2en[zh] = en.strip('\n')
    #        test[movie_title] = test.get(movie_title,0) + 1        
            
    #========= compute TFIDF ==========================        
    path4store = os.path.join('.','candidates')
    test_movie_name_list = os.listdir(path4testData)#[re.findall('(.*).txt',name)[0] for name in os.listdir(path4testData)]
    print(test_movie_name_list)
    movieNameList = os.listdir(path) 
    N = len (movieNameList)
    movie_tf = {}
    movie_idf = {}
    movie_tfidf = {}
    for movie_file in movieNameList:
        temp_dic = {}# for record weather a word appear in this movie
        #tf
        with open(os.path.join(path,movie_file),'r',encoding = 'utf-8') as f:#movie
            movie_name = re.findall('(.*).txt',movie_file)[0]
            for line in f:#sub
                line = line.strip('\n')
                #vocab,pos = line.split('\t')
                #temp_dic[vocab,pos] = 1
                temp_dic[line] = 1
                movie_tf[movie_name,line] = movie_tf.get(movie_name,0) + 1 
                #movie_idf[line] = movie_idf.get(line,0) += 1        
        for key in temp_dic:#idf
            movie_idf[key] = movie_idf.get(key,0) + 1
            
    for test_file in test_movie_name_list:
        temp_dic = {}# for record weather a word appear in this movie
        with open(os.path.join(path4testData,test_file),'r',encoding = 'utf-8') as f:#movie
            movie_name = re.findall('(.*).txt',test_file)[0]
            for line in f:#sub
                line = line.strip('\n')
                #vocab,pos = line.split('\t')
                #temp_dic[vocab,pos] = 1
                temp_dic[line] = 1
                movie_tf[movie_name,line] = movie_tf.get(movie_name,0) + 1 
                #movie_idf[line] = movie_idf.get(line,0) += 1        
        for key in temp_dic:#idf
            movie_idf[key] = movie_idf.get(key,0) + 1
            
    for item,value in movie_tf.items():#tfidf
        movie_tfidf[item[0]] = movie_tfidf.get(item[0],list([1])) +[ (item[1],movie_tf[item]*np.log2(N/movie_idf[item[1]])) ]
    for key in movie_tfidf:
        movie_tfidf[key].pop(0)
        #movie_tfidf
    #======write to .txt=============================    
    #words = {}
    #file_name = 'movie_tfidf_pos.txt'
    #for key in movie_tfidf:   
    #    movie_tfidf[key] = sorted(movie_tfidf[key],key = lambda x: x[1],reverse = True)
    #with open(os.path.join('.',file_name),'w',encoding = 'utf-8') as f:
    #    for key in movie_tfidf:   
    #        if key not in title_en2zh.keys():            
    #            f.write(key + '\n')
    #        else:
    #            f.write(title_en2zh[key] + '\n')
    #        for tfidf in movie_tfidf[key]:
    #            f.write(str(tfidf[0]) +'\t'+str(tfidf[1])+'\t')
    #        f.write('\n\n')                    
    #======classification by pos =============================        
    '''
    data struct.
    titleInfo{
         'movie name1':{
                          'NN':[(戰狼,9.22224),(將軍,5.22224),(你,2.22224)]
                          'VV':[((殺,9.22224),(親,5.22224))]
                              }
        'movie name2':{
                          'NN':[(戰狼,9.22224),(將軍,5.22224),(你,2.22224)]
                          'VV':[((殺,9.22224),(親,5.22224))]
                              }                  
    }
    input:movie_tfidf
    '''
    
    def movie_model(movie_tfidf):
        titleInfo = {}
        for movieName in movie_tfidf:#each movie
            tfidfbypos = {}
            for word_and_pos in  movie_tfidf[movieName]:#each words
                word,pos = word_and_pos[0].split('\t')
                tfidf = word_and_pos[1]
                if not tfidfbypos.get(pos,[]):#not appear in dictionary
                    tfidfbypos[pos] =  [(word,tfidf)]
                else:
                    tfidfbypos[pos] +=  [(word,tfidf)]
            for pos in tfidfbypos:
                tfidfbypos[pos] = sorted(tfidfbypos[pos],key = lambda x: x[1],reverse = True)
            titleInfo[movieName] = tfidfbypos
        return titleInfo
    
    titleInfo = movie_model(movie_tfidf)
    titleInfo[list(titleInfo.keys())[100]]    
    #====== find movie pattern =============================        
    #path4titlepos = r'C:\Users\順益\Desktop\106-NLP\final project'
    #file_name = 'newAllTitle_parsed_pos.txt'
    #pattern = {}
    
    #with open(os.path.join(path4titlepos,file_name),'r',encoding = 'utf-8') as f:
    #    for title_and_pos in f:
    #        list_title , list_pos = title_and_pos.split('\t')
    #        pattern[str(list_pos)] = pattern.get(list_pos,0) + 1 #count 
    
    #pattern_sorted_list = sorted(pattern.items(),key = lambda x: x[1], reverse = True)
    #for i,item in enumerate(pattern_sorted_list[:10]):
    #    print("[{}] {}".format(i+1,item))
    
    #====== find movie pattern =============================        
    '''
    input:pattern_sorted_list  :list
          num_canadate  :int       
          test_movie_name_list: list,element is the movie name which you want to test
    '''

    #num_candidate = 10
    #thr_tfidf = 8
    #test_movie_name_list = list(titleInfo.keys())[:5]# just for debug
    # titleInfo[list(titleInfo.keys())[0]].keys()
    #max_words_num = 20
    #pattern_sorted_list[:num_candidate]
    #thr_tfidf_min = 4
    #thr_tfidf_max = 8
    for movie_name in test_movie_name_list:#each movie    
        movie_name = re.findall('(.*).txt',movie_name)[0]
        list_NN = []
        list_VV = []
        list_JJ = []
        list_NR = []
        count = 0
        for i,item in enumerate(titleInfo[movie_name]['NN']):
            if count < max_words_num and item[1] > thr_tfidf_min and item[1] < thr_tfidf_max:
                list_NN.append(item[0])
                count += 1
        count = 0
        if 'VV' in titleInfo[movie_name].keys():            
            for i,item in enumerate(titleInfo[movie_name]['VV']):
                if i < max_words_num and item[1] > thr_tfidf_min and item[1] < thr_tfidf_max:
                    list_VV.append(item[0])
                    count += 1
        count = 0            
        if 'NR' in titleInfo[movie_name].keys():
            for i,item in enumerate(titleInfo[movie_name]['NR']):
                if i < max_words_num and item[1] > thr_tfidf_min and item[1] < thr_tfidf_max:
                    list_NR.append(item[0])
                    count += 1
        count = 0            
        if 'JJ' in titleInfo[movie_name].keys():
            for i,item in enumerate(titleInfo[movie_name]['JJ']):
                if i < max_words_num and item[1] > thr_tfidf_min and item[1] < thr_tfidf_max:
                    list_JJ.append(item[0])
                    count += 1
        
        candidate_titles = []
        condidate_titles_NNNN = []
        for item1 in list_NN:
            for item2 in list_NN:
                if item1 != item2:
                    condidate_titles_NNNN.append(item1+" "+item2)
        candidate_titles += condidate_titles_NNNN
        
        condidate_titles_NN = []
        for item1 in list_NN:    
            condidate_titles_NN.append(item1)
        candidate_titles += condidate_titles_NN
            
        condidate_titles_NR = []
        for item1 in list_NR:    
            condidate_titles_NR.append(item1)
        candidate_titles += condidate_titles_NR
            
        condidate_titles_VVNN = []
        for item1 in list_VV:    
            for item2 in list_NN:
                condidate_titles_VVNN.append(item1+" "+item2)
        candidate_titles += condidate_titles_VVNN
                
        condidate_titles_JJNN = []
        for item1 in list_JJ:    
            for item2 in list_NN:    
                condidate_titles_JJNN.append(item1+" "+item2)
        candidate_titles += condidate_titles_JJNN
                
        condidate_titles_NRNN = []
        for item1 in list_NR:    
            for item2 in list_NN:
                condidate_titles_NRNN.append(item1+" "+item2)
        candidate_titles += condidate_titles_NRNN
        
        condidate_titles_NNVV = []
        for item1 in list_NN:    
            for item2 in list_VV:    
                condidate_titles_NNVV.append(item1+" "+item2)
        candidate_titles += condidate_titles_NNVV
                
        condidate_titles_NNNNNN = []
        for item1 in list_NN:    
            for item2 in list_NN:
                for item3 in list_NN:
                    if item1 != item2 and item1 != item3 and item3 != item2:
                        condidate_titles_NNNNNN.append(item1+" "+item2+" "+item3)        
        candidate_titles += condidate_titles_NNNNNN
                    
        condidate_titles_NNVVNN = []
        for item1 in list_NN:    
            for item2 in list_VV:
                for item3 in list_NN:
                    condidate_titles_NNVVNN.append(item1 +" "+item2+" "+item3)        
        candidate_titles += condidate_titles_NNVVNN
                
        with open(os.path.join(path4store,movie_name+'.txt'),'w',encoding = 'utf-8') as f:
            for title in candidate_titles:
                #print(title+'\n')
                for word in title.split():
                    f.write(word)
                f.write('\t'+title+'\n')
            
    print("generate title finished!!! === time:{:.3f}".format(time.time()-t_start))

if __name__ == '__main__':    
    gen_candidate_title(thr_tfidf_max = 11,thr_tfidf_min = 8 ,max_words_num = 20,num_candidate = 10,thr_tfidf = 8,path = os.path.join('.','pos'),path4testData = os.path.join('.','postxt'))

        
'''
Created on Tue Jan  9 18:51:54 2018
@author: Pan
movie_tfidf_pos.txt
'''
#assume the path and file exist:    
#path4moviefile ==== C: Users 順益 Desktop 106-NLP final project embedding_input3(pos)