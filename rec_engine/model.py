import os
from typing import List

import pandas as pd

from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")
from dotenv import load_dotenv

load_dotenv()


class NewsTMModel:

    def __init__(self, topic_model=None):
        russian_stopwords = stopwords.words("russian")
        vectorizer_model = CountVectorizer(stop_words=russian_stopwords)
        self.topic_model = topic_model or BERTopic(verbose=True,
                                                   language='multilingual',
                                                   diversity=0.2, vectorizer_model=vectorizer_model,
                                                   nr_topics=50)

    def fit(self, data: pd.DataFrame):
        text_data = (data.title + ". " + data.summary).to_list()
        self.topic_model = self.topic_model.fit(text_data)

    def predict(self, data: pd.DataFrame):
        text_data = (data.title + ". " + data.summary).to_list()
        topics, probs = self.topic_model.transform(text_data)
        return topics, probs

    def get_topics_over_time(self, data: pd.DataFrame, nr_bins=20):
        text_data = (data.title + ". " + data.summary).to_list()
        timestamps = data.publication_datetime.to_list()
        topics_over_time = self.topic_model.topics_over_time(text_data,
                                                             timestamps=timestamps,
                                                             nr_bins=nr_bins)
        return topics_over_time

    def find_topics(self, search_term, thrsh=0.5, top_n=5):
        topics, probs = self.topic_model.find_topics(search_term, top_n=top_n)
        topic_ids = [topic for topic, prob in zip(topics, probs) if prob > thrsh]
        topics_labels = self.topic_model.generate_topic_labels()
        topic_names = [topics_labels[topic_id+1] for topic_id in topic_ids]
        return search_term, topic_names

    def save(self, model_path):
        self.topic_model.save(model_path)

    def load(self, model_path):
        self.topic_model = self.topic_model.load(model_path)
