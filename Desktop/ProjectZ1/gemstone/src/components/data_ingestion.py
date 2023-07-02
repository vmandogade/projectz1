import os    # to create path, to join path, while deploying the model on linux  os is imp.
import sys    #for sys error
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass    #when u just want to create instance variable, and not functions within class then,
                                      # we use dataclass
from src.components.data_transformation import DataTransformation


## Intitialize the Data Ingetion Configuration

@dataclass
class DataIngestionconfig:  #this class is created to stored the output of data ingestion
    train_data_path:str=os.path.join('artifacts','train.csv')  #it will create artifacts folder with train.csv inside it
    test_data_path:str=os.path.join('artifacts','test.csv')  #it will create artifacts folder with test.csv inside it
    raw_data_path:str=os.path.join('artifacts','raw.csv')  #it will create artifacts folder with raw.csv inside it

## create a class for Data Ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()  #all 3 paths are stored inside self.ingestion_config

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods Starts')
        try:
            df=pd.read_csv(os.path.join('notebooks/data','gemstone.csv')) #data source can be anything
            logging.info('Dataset read as pandas Dataframe')  #reading from particular source

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)  # creating artifact folder inside local directory. if exist then keep folder
            df.to_csv(self.ingestion_config.raw_data_path,index=False)  # saving converted csv source file into newly created artifact folder. no additinal index will create
            logging.info('Train test split')  
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42) #splitting raw data into train-test csv

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) #train csv is stored in train_data_path
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True) #test csv is stored in test_data_path

            logging.info('Ingestion of Data is completed')

            return(
                self.ingestion_config.train_data_path,  #finally returning train data stored inside train_data_path
                self.ingestion_config.test_data_path #finally returning test data stored inside test_data_path
            )
  
            
        except Exception as e:
            logging.info('Exception occured at Data Ingestion stage')
            raise CustomException(e,sys)
        

        ## You can use folowing code to run data_ingetsion and data_transformation code in local system
        
#if __name__=='__main__':
    #obj=DataIngestion()
    #train_data,test_data=obj.initiate_data_ingestion()



#if __name__=='__main__':
    #obj=DataIngestion()  #object created for DataIngestion class
    #train_data_path,test_data_path=obj.initiate_data_ingestion() # WKT, to access function we need to create object.
    #data_transformation = DataTransformation()   #object created for DataTransformation class so that we can access initiate_data_transformation function
    #train_arr, test_arr,_ = data_transformation.initaite_data_transformation(train_data_path,test_data_path)  # to avoid 'too many values to unpack' error. wrote '_'.