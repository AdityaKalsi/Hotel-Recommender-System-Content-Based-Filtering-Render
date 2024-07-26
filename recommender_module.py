import joblib
import pandas
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    df_final = pickle.load(open('df_final.pkl', 'rb'))
except FileNotFoundError:
    raise FileNotFoundError("The file 'df_final.pkl' was not found.")
except Exception as e:
    raise RuntimeError(f"An error occurred while loading the file: {e}")


tfidf = TfidfVectorizer(max_features=1000)

def recommend(type,country,city,property):
    
    ## filtering the dataframe to the requirements of the user
    filtered_df = df_final[
        (df_final['roomtype'] == type) &
        (df_final['country'] == country) &
        (df_final['city'] == city) &
        (df_final['propertytype'] == property)
    ]

    ## creating a temporary dataframe so that we recommend hotels only from the speicified country and city rather than using the entire df which
    ## could lead to results from different cities and countries
    temp = df_final[
        (df_final['country'] == country) &
        (df_final['city'] == city) 
    ]

    ## indices of the hotels of user requirements
    idx1 = filtered_df['index'].tolist()

    ## reseting index because we need to search for the indices in idx1 in temp
    temp.reset_index(inplace = True)

    ## extracting the index(of the dataframe) of the specified hotels 
    idx2 = temp[temp['index'].isin(idx1)].index.tolist()
    
    ## creating similarity matrix
    vector = tfidf.fit_transform(temp['tags']).toarray()
    similarity = cosine_similarity(vector)
    
    ## traverse each user specified hotel and extract top recommend hotels for each specified hotel
    recommendations = set()
    for i in idx2:
        similar_hotels = sorted(list(enumerate(similarity[i])),key = lambda x:x[1],reverse = True)[0:5]
        for hotel in similar_hotels:
             recommendations.add(tuple(temp.loc[hotel[0]][['hotelname','roomtype','starrating']]))
    return list(recommendations)