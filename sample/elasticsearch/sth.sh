curl -XPUT -H "Content-Type: application/json" -d '{"transient":{"cluster":{"max_shards_per_node":10000}}}' 'http://172.30.5.211:9200/_cluster/settings'
