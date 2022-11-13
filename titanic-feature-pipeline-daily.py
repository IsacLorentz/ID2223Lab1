import os
import modal
    
BACKFILL=False
LOCAL=True

if LOCAL == False:
   stub = modal.Stub()
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","sklearn","dataframe-image"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("id2223-lab1"))
   def f():
       g()


def sample_passenger():
    """
    Returns a single iris flower as a single row in a DataFrame
    """
    import pandas as pd
    import random
    import hopsworks
    import numpy as np

    # You have to set the environment variable 'HOPSWORKS_API_KEY' for login to succeed
    project = hopsworks.login()
    # fs is a reference to the Hopsworks Feature Store
    fs = project.get_feature_store()

    # titanic_fg = fs.get_feature_group(name="titanic_modal", version=1)
    #query = titanic_fg.select_all()
    feature_view = fs.get_feature_view(name="titanic_modal",
                                        version=1)  
    X_train, X_test, y_train, y_test = feature_view.train_test_split(0.005)
    print('X_train: ', type(X_train))
    df = pd.DataFrame({ "pclass": [np.random.choice(X_train['pclass'].astype('category').cat.codes)],
                       "sex": [np.random.choice(X_train['sex'].astype('category').cat.codes)],
                       "age": [np.random.choice(X_train['age'])],
                       "sibs": [np.random.choice(X_train['sibs'])],
                       "par_ch": [np.random.choice(X_train['par_ch'])],
                       "fare": [np.random.choice(X_train['fare'])],
                       "deck": [np.random.choice(X_train['deck'].astype('category').cat.codes)],
                       "embarked": [np.random.choice(X_train['embarked'].astype('category').cat.codes)],
                      })
    survived = np.random.choice(y_train['survived'])
    #print('df: ', df)
    print('survived: ',survived)
    df['survived'] = survived
    return df

# def generate_flower(name, sepal_len_max, sepal_len_min, sepal_width_max, sepal_width_min, 
#                     petal_len_max, petal_len_min, petal_width_max, petal_width_min):
#     """
#     Returns a single iris flower as a single row in a DataFrame
#     """
#     import pandas as pd
#     import random

#     df = pd.DataFrame({ "sepal_length": [random.uniform(sepal_len_max, sepal_len_min)],
#                        "sepal_width": [random.uniform(sepal_width_max, sepal_width_min)],
#                        "petal_length": [random.uniform(petal_len_max, petal_len_min)],
#                        "petal_width": [random.uniform(petal_width_max, petal_width_min)]
#                       })
#     df['variety'] = name
#     return df

# def get_random_iris_flower():
#     """
#     Returns a DataFrame containing one random iris flower
#     """
#     import pandas as pd
#     import random

#     virginica_df = generate_flower("Virginica", 8, 5.5, 3.8, 2.2, 7, 4.5, 2.5, 1.4)
#     versicolor_df = generate_flower("Versicolor", 7.5, 4.5, 3.5, 2.1, 3.1, 5.5, 1.8, 1.0)
#     setosa_df =  generate_flower("Setosa", 6, 4.5, 4.5, 2.3, 1.2, 2, 0.7, 0.3)

#     # randomly pick one of these 3 and write it to the featurestore
#     pick_random = random.uniform(0,3)
#     if pick_random >= 2:
#         iris_df = virginica_df
#         print("Virginica added")
#     elif pick_random >= 1:
#         iris_df = versicolor_df
#         print("Versicolor added")
#     else:
#         iris_df = setosa_df
#         print("Setosa added")

#     return iris_df



def g():
    
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()

    if BACKFILL == True:
        iris_df = pd.read_csv("https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1/titanic.csv")
    else:
       titanic_df = sample_passenger()

    titanic_fg = fs.get_feature_group(
        name="titanic_modal",
        version=1)
    titanic_fg.insert(titanic_df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()
