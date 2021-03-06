# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nnldz28-D_1p4Fi6Xul5tcz-uZpfaJoe
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def content_base_recommendation(filePath, keyword):
    df = pd.read_csv(filePath)
    for i in df.columns.values:

        if i != 'keyword1' and i != 'title' and i != 'update_date' and i != 'Source' and i != 'authors':
            del df[i]
    item_user_likes = keyword
    new = pd.DataFrame({'keyword1': item_user_likes, 'title': '1'
                        }, index=[len(df)]
                       )
    df = df.append(new, ignore_index=True)

    features = {'keyword1'}

    def combine_features(row):
        return row['keyword1']

    for feature in features:
        df[feature] = df[feature].fillna('')
    df['combined_features'] = df.apply(combine_features, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix[len(df['combined_features']) - 1])

    similar_movies = list(enumerate(cosine_sim))

    def get_title_from_index(index):
        return df[df.index == index]["title"].values

    def get_index_from_title(index):
        return df[df.index == index]

    # output is get_title_from_index(element[0])
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
    for i in df.columns.values:
        if i != 'title' and i != 'update_date' and i != 'Source' and i != 'authors':
            del df[i]
    if sorted_similar_movies[0][1] < 0.1:
        df4 = pd.DataFrame({'title': [], 'update_date': [], 'Source': [], 'authors': []})
        return df4
    else:
        i = 0
        # print("Top 10 similar movies to "+item_user_likes+" are:\n")
        for element in sorted_similar_movies:
            if i == 0:
                df4 = pd.DataFrame(get_index_from_title(element[0]))
                i += 1
            else:
                if get_title_from_index(element[0]) != '1' and element[1] > 0.1:
                    df5 = pd.DataFrame(get_index_from_title(element[0]))
                    df4 = pd.concat([df4, df5])
                    i = i + 1
                    if i > 10:
                        break
        return df4


# print(content_base_recommendation(filepath="G:\download\cs.CL3.csv" ,keyword="spchee recognition"))
if __name__ == '__main__':
    filepath = input("please input your filepath ")
    keyword = input("please input your keyword ")
    print(content_base_recommendation(filePath=filepath, keyword=keyword))
    # content_base_recommendation(filePath=filepath ,keyword=keyword)
