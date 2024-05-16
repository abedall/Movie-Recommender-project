import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from web.models import Myrating, Movie
from django.db.models import Case, When

def Myrecommend():
    # Load data from Django model into a pandas dataframe
    df = pd.DataFrame(list(Myrating.objects.all().values()))

    # Handle duplicate user-movie pairs by averaging the ratings
    df = df.groupby(['user_id', 'movie_id'], as_index=False).rating.mean()

    # Create a user-item matrix
    user_movie_matrix = df.pivot(index='movie_id', columns='user_id', values='rating').fillna(0)

    # Fit the SVD model
    svd = TruncatedSVD(n_components=20, random_state=42)
    svd_matrix = svd.fit_transform(user_movie_matrix)

    # Compute the prediction matrix
    predicted_ratings = np.dot(svd_matrix, svd.components_)
    
    # Normalization
    Ymean = np.mean(predicted_ratings, axis=1).reshape(-1, 1)
    my_predictions = predicted_ratings + Ymean

    return my_predictions, Ymean
