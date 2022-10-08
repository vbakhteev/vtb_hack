cd news && scrapy crawl rbc -o /data/rbc_lines.jsonl -t jsonlines && scrapy crawl buh -o /data/buh_items.jsonl -t jsonlines && scrapy crawl consultant -o /data/consultant_items.jsonl -t jsonlines
