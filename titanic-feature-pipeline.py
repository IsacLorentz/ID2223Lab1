import os

import modal

LOCAL=True

if LOCAL == False:
   stub = modal.Stub()
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","sklearn","dataframe-image"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("id2223-lab1"))
   def f():
       g()

def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()
    titanic_df = pd.read_csv("https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1/titanic.csv")
    
    # data preprocessing
    
    # print(titanic_df)
    # titanic_df = titanic_df.dropna(axis=1)
    # print(titanic_df)
    titanic_df['Deck'] = titanic_df['Cabin'].str.extract(r'([A-Z])?(\d)')[0]

    titanic_df.reset_index(drop=True)
    # titanic_df['PassengerId'] = titanic_df.index
    titanic_df = titanic_df[['Pclass','Sex','Age','SibSp','Parch','Fare','Deck','Embarked','Survived']].copy()
    titanic_df.columns = ['pclass','sex','age','sibs','par_ch','fare','deck','embarked','survived']
    titanic_df['age'] = titanic_df['age'].fillna(titanic_df['age'].mean())
    titanic_df['fare'] = titanic_df['fare'].fillna(titanic_df['fare'].mean())

    titanic_df['embarked'] = titanic_df['embarked'].fillna(titanic_df['embarked'].mode())
    titanic_df['deck'] = titanic_df['deck'].fillna(0)

    titanic_df['pclass'] = titanic_df['pclass'].astype('category').cat.codes
    titanic_df['sex'] = titanic_df['sex'].astype('category').cat.codes
    titanic_df['deck'] = titanic_df['deck'].astype('category').cat.codes
    titanic_df['embarked'] = titanic_df['embarked'].astype('category').cat.codes

    titanic_df['age'] = (titanic_df['age'] - titanic_df['age'].mean()) / titanic_df['age'].std()
    titanic_df['fare'] = (titanic_df['fare'] - titanic_df['fare'].mean()) / titanic_df['fare'].std()


    # print(titanic_df.isna().any())
    
    titanic_fg = fs.get_or_create_feature_group(
        name="titanic_modal",
        version=1,
        #fix primary key
        primary_key=["pclass", "sex", "age", "sibs", "par_ch", "fare", "deck", "embarked"], 
        description="titanic passengers dataset")
    titanic_fg.insert(titanic_df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()
