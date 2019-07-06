import os
import sys
from os import listdir
import jieba
import jieba.posseg as pseg
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

def recommand(movieName,movieKind):
    #movieName = movieName+" (豆瓣)"
    flag = 0 #指示目标电影的标签
    label_ = []
    label = [label_]*10 #分成十类
    all_file=listdir('D:/temp/data2') #获取文件夹中所有文件名
    #all_file = listdir('D:/temp/data1/动作')
    labels=[] #用以存储电影名称
    corpus=[] #空语料库
    '''停用词的过滤'''
    typetxt=open('D:/temp/stop/stop.txt',encoding='utf-8')
    texts=['\u3000','\n',' '] #爬取的文本中未处理的特殊字符

    '''停用词库的建立'''
    for word in typetxt:
        word=word.strip()
        texts.append(word)

    '''语料库的建立'''
    for i in range(0,len(all_file)):
        filename=all_file[i]
        filelabel=filename.split('.')[0]
        labels.append(filelabel) #电影名称列表
        file_add='D:/temp/data2/'+ filename
        #file_add = 'D:/temp/data1/动作/' + filename
        doc=open(file_add,encoding='utf-8').read()
        data=jieba.cut(doc) #文本分词
        data_adj=''
        delete_word=[]
        for item in data:
            if item not in texts: #停用词过滤
                data_adj+=item+' '
            else:
                delete_word.append(item)
        corpus.append(data_adj) #语料库建立完成

    '''输出语料库'''
    '''boc = open('D:/temp/output/corpus1.txt','w',encoding='utf-8')
    print (corpus, file = boc)'''


    '''计算td-idf值'''
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    '''k-means聚类分析'''
    mykms=KMeans(n_clusters=10)
    y=mykms.fit_predict(weight)
    for i in range(0,10):
        label[i]=[]
        for j in range(0,len(y)):
            if y[j]==i:
                #temp = labels[j][0:(len(labels[j])-5)]
                filename1 = labels[j].split('[')[0]
                label[i].append(labels[j])
                if filename1 == movieName:
                    flag = i
        print('label_'+str(i)+':'+str(label[i]))

    print ('label_'+str(flag))
    result = []
    #result = "出错"
    for m in range(0,len(label[flag])):
        #print(label[flag][m])
        filename2 = label[flag][m].split('[')
        name = filename2[0]
        kind = filename2[1:2]
        kind = ''.join(kind)
        kind = kind.split(',')
        #print(name + str(kind))
        #for q in range(len(kind)):
            #print(name+kind[q])
        flagflag = 0
        if name != movieName:
            for q in range(len(kind)):
                if (kind[q][1:3] == movieKind) | (kind[q][2:4] == movieKind) | (movieKind == '全部'):
                    flagflag = 1
        if (flagflag == 1):
            result.append(name)

    #print(result)
    #print(movieName)

    '''输出标志词以及每一类的文本'''
    doc = open('D:/temp/output/dis/output_flag.txt', 'w')
    for i in range(len(weight)):
        if y[i]==flag:
            print("这里输出第" + str(i) + "类文本的词语tf-idf权重" + " 电影名称是" + str(labels[i]), file=doc)
            for j in range(len(word)):
                if (weight[i][j] != 0):
                    print(word[j], weight[i][j], file=doc)

    return result


