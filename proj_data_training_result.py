
""" 데이터를 트레이닝 시키고 테스트까지 하는 모듈.
    python [모듈이름] [연예 관련기사 개수] [정치 관련기사 개수]
"""

import sys
import os
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
#from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.linalg import Vectors
#from pyspark.mllib.linalg import Vectors,VectorUDT
from pyspark.sql import Row
import pyspark

def init_pyspark():
    os.environ["SPARK_HOME"]=os.path.join('C:\Users\Chan\Downloads\spark-2.0.0-bin-hadoop2')
    os.environ["PYLIB"]=os.path.join(os.environ["SPARK_HOME"],'python','lib')
    sys.path.insert(0,os.path.join(os.environ["PYLIB"],'py4j-0.10.1-src.zip'))
    sys.path.insert(0,os.path.join(os.environ["PYLIB"],'pyspark.zip'))


myConf=pyspark.SparkConf()
spark = pyspark.sql.SparkSession.builder\
    .master("local")\
    .appName("myApp")\
    .config(conf=myConf)\
    .config('spark.sql.warehouse.dir','file:///C:/Users/Chan/code/s_201211274/data')\
    .getOrCreate()


def do_machine_learning(enterteinment_num,politics_num):
    _fp=os.path.join(os.getcwd()+'/result_articles.txt')     #크롤링을 통해 얻은 트레이닝 데이터를 불러옴.
    _f=open(_fp,'r')

    frame=[]
    while True:
        line = _f.readline()
        if not line: 
            break
        temp=[]
        for node in line.split():
            temp.append(node)
        frame.append(temp)
        print(temp)
    _f.close()   
    ###############
    df = spark.createDataFrame(frame,['cls','entertainment','politics'])
    clsIndexer = StringIndexer(inputCol="cls", outputCol="label")                          
    i1Indexer = StringIndexer(inputCol="entertainment", outputCol="i1")
    i2Indexer = StringIndexer(inputCol="politics", outputCol="i2")

    va = VectorAssembler(inputCols=["i1","i2"],outputCol="features")
    pipeline = Pipeline(stages=[clsIndexer,i1Indexer,i2Indexer,va])
    
    model = pipeline.fit(df)
    df2 = model.transform(df)
    df2.printSchema()
    df2.show()

    trainDf=df2.select('label','features')
    
    lr = LogisticRegression(maxIter=10, regParam=0.01)
    lrModel = lr.fit(trainDf)           #트레이닝 데이터 생성

    #print Vectors.dense(10,10)
    test0 = spark.sparkContext.parallelize([Row(features=Vectors.dense([enterteinment_num,politics_num]))]).toDF()   #테스트 데이터 입력
    result = lrModel.transform(test0).head()
    print "Irregularity ? : ",result.prediction


if __name__ == '__main__':
    
    
    init_pyspark()
    #do_machine_learning(sys.argv[1],sys.argv[2])
    do_machine_learning(1,1)
    
    