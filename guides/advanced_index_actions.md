from opensearchpy import OpenSearch

# Setup
client = OpenSearch(
    hosts=['https://admin:admin@localhost:9200'],
    verify_certs=False
)

index_name = "movies"

# Create index
client.indices.create(index=index_name)

# API Actions
## Clear index cache
client.indices.clear_cache(index=index_name)

## Flush index
client.indices.flush(index=index_name)

## Refresh index
client.indices.refresh(index=index_name)

## Open/Close index
client.indices.close(index=index_name)
client.indices.open(index=index_name)

## Force merge index
client.indices.forcemerge(index=index_name)

## Clone index
client.indices.put_settings(index=index_name, body={ "index": { "blocks": { "write": True } } })
client.indices.add_block(index=index_name, block="write")
client.indices.clone(index=index_name, target="movies_clone")
client.indices.put_settings(index=index_name, body={ "index": { "blocks": { "write": False } } })

## Split index
client.indices.create(
    index="books",
    body={
        "settings": {
            "index": {
                "number_of_shards": 5,
                "number_of_routing_shards": 30,
                "blocks": {
                    "write": True
                }
            }
        }
    }
)

client.indices.split(
    index="books",
    target="bigger_books",
    body={
        "settings": {
            "index": {
                "number_of_shards": 10
            }
        }
    }
)

client.indices.put_settings(index="books", body={ "index": { "blocks": { "write": False } } })

# Cleanup
client.indices.delete(index=[index_name, "books", "movies_clone", "bigger_books"])
