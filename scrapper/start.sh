cd news && scrapy crawl consultant -o /data/consultant_items.jsonl -t jsonlines && scrapy crawl rbc -o /data/rbc_items.jsonl -t jsonlines
