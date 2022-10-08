import requests
from typing import Literal
from urllib.parse import urljoin


Role = Literal["manager", "accountant"]


class ApiClient:
    def __init__(self, url):
        self.url = url

    def get_topics(self, role_name: Role):
        topics = self._get(
            'topics',
            {'role_name': role_name},
        )

        return topics
    
    def get_publications(self, topic_id: int, num: int):
        publications = self._get(
            'publications',
            {'topic_id': topic_id, 'num': num},
        )
        return publications

    def get_trend(self, topic_id: int):
        trend = self._get(
            'trend',
            {'topic_id': topic_id}
        )
        return trend["frequency"]
    
    def search(self, query, num: int, role_name: Role):
        publications = [
            {
                'title': 'Расчеты и налоги в октябре: на что обратить внимание',
                'text': '1. Электронные счета-фактуры по госконтрактам с 1 октября\n\nчерез единую информационную систему в сфере закупок.\n\n2. С IV квартала российские организации и ИП\n\nпри покупке у зарубежных компаний электронных услуг с местом реализации в России. Исключение — иностранная организация оказывает такие услуги через обособленное подразделение в России. Если до 1 октября была перечислена предоплата (с НДС), обязанность\xa0налогового агента\n\n.\n\n3. ФНС сообщила\n\n, которые можно использовать при заполнении декларации по НДС. В частности, речь идет об операциях по передаче исключительных прав по договору коммерческой концессии.\n\nОктябрь — последний месяц, когда многие организации и предприниматели\n\nстраховые взносы. Крайний срок уплаты взносов за сентябрь перенесен на год (на\n\n).\n\nНапомним, мера поддержки затрагивает тех, кто работает в установленных правительством\n\n(строительство, перевозки, гостиничный бизнес, общепит и т.д.),\n\n.\n\nС\n\nобновили\n\nоб открытии обособленного подразделения (кроме филиала и представительства). Для абсолютного большинства организаций и предпринимателей изменения носят технический характер.\n\nС 17 октября\n\nформат электронного акта о приемке строительных работ. Использование электронных актов позволит оптимизировать документооборот. Кроме того, их можно будет представлять при подготовке ответа на требования налоговиков или при даче им пояснений.\n\n31 октября — крайний срок уплаты налога за 2021 год для организаций, которые весной получили полугодовую\n\n.\n\n1. С 1 октября перестала\xa0действовать льгота, позволявшая ввозить и продавать немаркированные наборы, которые включают\n\nили\n\n.\n\n2.\xa0С 3 октября\n\nк маркировке молочной продукции. Ее можно начинать продавать, не дожидаясь передачи информации в систему "Честный знак". Передать информацию нужно в течение 3 рабочих дней с момента приемки партии маркированной продукции. Послабления будут действовать до 1 июня 2025 года.\n\n1. С 3 октября действует обновленная рекомендуемая\n\nучреждений. В форму добавили строку для отражения показателей по КВР\n\n.\n\n2. После 1 октября федеральные ПБС могут принимать бюджетные обязательства по закупкам только в\n\n. Минфин\n\n, какие КБК соответствуют таким закупкам. Ведомство также сообщило, по\n\nс 2 октября не будут приостанавливать операции на лицевых счетах. Например, это касается закупок за счет резервных фондов президента и правительства.\n\n3.\xa0Особых указаний по отчетности на 1 октября в этом году нет.\xa0Напомним основные правила и нюансы: что делать, если последний день срока для отчета выпадает на выходной, каков состав отчетности и какие отчеты можно не подавать. Подробности в\n\n.' ,
                'url': 'http://www.consultant.ru/legalnews/20471/',
                'publication_datetime': '8 Окт 23:23',
            },
            {
                'title': 'Обзор новых антикризисных мер за 24 – 30 сентября',
                'text': '1. Электронные счета-фактуры по госконтрактам с 1 октября\n\nчерез единую информационную систему в сфере закупок.\n\n2. С IV квартала российские организации и ИП\n\nпри покупке у зарубежных компаний электронных услуг с местом реализации в России. Исключение — иностранная организация оказывает такие услуги через обособленное подразделение в России. Если до 1 октября была перечислена предоплата (с НДС), обязанность\xa0налогового агента\n\n.\n\n3. ФНС сообщила\n\n, которые можно использовать при заполнении декларации по НДС. В частности, речь идет об операциях по передаче исключительных прав по договору коммерческой концессии.\n\nОктябрь — последний месяц, когда многие организации и предприниматели\n\nстраховые взносы. Крайний срок уплаты взносов за сентябрь перенесен на год (на\n\n).\n\nНапомним, мера поддержки затрагивает тех, кто работает в установленных правительством\n\n(строительство, перевозки, гостиничный бизнес, общепит и т.д.),\n\n.\n\nС\n\nобновили\n\nоб открытии обособленного подразделения (кроме филиала и представительства). Для абсолютного большинства организаций и предпринимателей изменения носят технический характер.\n\nС 17 октября\n\nформат электронного акта о приемке строительных работ. Использование электронных актов позволит оптимизировать документооборот. Кроме того, их можно будет представлять при подготовке ответа на требования налоговиков или при даче им пояснений.\n\n31 октября — крайний срок уплаты налога за 2021 год для организаций, которые весной получили полугодовую\n\n.\n\n1. С 1 октября перестала\xa0действовать льгота, позволявшая ввозить и продавать немаркированные наборы, которые включают\n\nили\n\n.\n\n2.\xa0С 3 октября\n\nк маркировке молочной продукции. Ее можно начинать продавать, не дожидаясь передачи информации в систему "Честный знак". Передать информацию нужно в течение 3 рабочих дней с момента приемки партии маркированной продукции. Послабления будут действовать до 1 июня 2025 года.\n\n1. С 3 октября действует обновленная рекомендуемая\n\nучреждений. В форму добавили строку для отражения показателей по КВР\n\n.\n\n2. После 1 октября федеральные ПБС могут принимать бюджетные обязательства по закупкам только в\n\n. Минфин\n\n, какие КБК соответствуют таким закупкам. Ведомство также сообщило, по\n\nс 2 октября не будут приостанавливать операции на лицевых счетах. Например, это касается закупок за счет резервных фондов президента и правительства.\n\n3.\xa0Особых указаний по отчетности на 1 октября в этом году нет.\xa0Напомним основные правила и нюансы: что делать, если последний день срока для отчета выпадает на выходной, каков состав отчетности и какие отчеты можно не подавать. Подробности в\n\n.',
                'url': 'http://www.consultant.ru/legalnews/20464/',
                'publication_datetime': '8 Окт 23:23',
            }
        ]
        tags = ["война", "ковид"]
        return publications, tags

    def _get(self, endpoint, params):
        response = requests.get(
            urljoin(self.url, endpoint),
            params=params
        )
        response.raise_for_status()

        return response.json()
