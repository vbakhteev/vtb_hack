from model import NewsTMModel

from utils import DataLoader


def train_example():
    data_loader = DataLoader()
    data = data_loader.get_publications_over_period_by(sources=('RBC',),
                                                       date_start='2022-06-01',
                                                       date_end='2022-10-10'
                                                       )
    model = NewsTMModel()
    model.fit(data)
    return data, model


def predict_example(data, model):
    topics, probs = model.predict(data)
    return topics, probs


def topics_over_time_example(data, model):
    topics_over_time = model.get_topics_over_time(data)
    return topics_over_time


if __name__ == '__main__':
    data, model = train_example()
    print(predict_example(data, model))
    print(topics_over_time_example(data, model))
