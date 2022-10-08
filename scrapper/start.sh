cd news
scrapy crawl rbc -o /data/rbc_items.jsonl -t jsonlines
scrapy crawl buh -o /data/buh_items.jsonl -t jsonlines
scrapy crawl consultant -o /data/consultant_items.jsonl -t jsonlines
cd ..
echo "Dumping data to db"
bash dump_articles_to_db.sh
echo "Success"
