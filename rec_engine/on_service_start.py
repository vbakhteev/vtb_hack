from model import NewsTMModel
from utils import DataLoader


class NewsTopicAssessor:

    def __init__(self, businessman_model_path, accounter_model_path):
        self.businessman_model = NewsTMModel()
        self.businessman_model.load(businessman_model_path)
        self.accounter_model = NewsTMModel()
        self.accounter_model.load(accounter_model_path)
        data = DataLoader().get_data_with_unnassigned_topics()
        self.business_news = data.query("source=='RBC'").iloc[:100] #TODO: поменять на проде
        self.accounter_news = data.query("source!='RBC'").iloc[:100] #TODO: поменять на проде

    def get_topic_labels_for_businessman(self):
        return self.businessman_model.topic_model.generate_topic_labels()

    def get_topic_labels_for_accounter(self):
        return self.accounter_model.topic_model.generate_topic_labels()

    def label_business_news(self):
        topics, probs = self.businessman_model.predict(self.business_news)
        self.business_news['topic_id'] = topics
        return self.business_news

    def label_accounter_news(self):
        topics, probs = self.accounter_model.predict(self.business_news)
        self.accounter_news['topic_id'] = topics
        return self.accounter_news

if __name__ == '__main__':
    news_topic_assessor = NewsTopicAssessor("weights/rbc_tm", "weights/buh_tm")
    print(news_topic_assessor.get_topic_labels_for_businessman())
    print(news_topic_assessor.get_topic_labels_for_accounter())
    print("=======================================")
    print(news_topic_assessor.label_business_news())
    print(news_topic_assessor.label_accounter_news())





