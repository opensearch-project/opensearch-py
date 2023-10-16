from opensearchpy import OpenSearch
import time


# For cleaner output, comment in the two lines below to disable warnings and informational messages
# import urllib3
# urllib3.disable_warnings()


def test_opensearch_examples():
    # Set up
    client = OpenSearch(
        hosts=['https://localhost:9200'],
        use_ssl=True,
        verify_certs=False,
        http_auth=('admin', 'admin')
    )
    client.indices.create(index='movies')
    print("'movies' index created!")
    
    # Test Clear Index Cache
    client.indices.clear_cache(index='movies')
    print("Cache for 'movies' index cleared!")
    client.indices.clear_cache(index='movies', query=True)
    print("Query cache for 'movies' index cleared!")
    client.indices.clear_cache(index='movies', fielddata=True, request=True)
    print("Field data and request cache for 'movies' index cleared!")
    
    # Test Flush Index
    client.indices.flush(index='movies')
    print("'movies' index flushed!")
    
    # Test Refresh Index
    client.indices.refresh(index='movies')
    print("'movies' index refreshed!")
    
    # Test Close or Open Index
    client.indices.close(index='movies')
    print("'movies' index closed!")
    time.sleep(2)  # add sleep to ensure the index has time to close
    client.indices.open(index='movies')
    print("'movies' index opened!")
    
    # Test Force Merge Index
    client.indices.forcemerge(index='movies')
    print("'movies' index force merged!")
    
    # Test Clone
    client.indices.put_settings(index='movies', body={'index': {'blocks': {'write': True}}})
    print("Write operations blocked for 'movies' index!")
    time.sleep(2)
    client.indices.clone(index='movies', target='movies_clone')
    print("'movies' index cloned to 'movies_clone'!")
    client.indices.put_settings(index='movies', body={'index': {'blocks': {'write': False}}})
    print("Write operations enabled for 'movies' index!")
    
    # Test Split 
    client.indices.create(
        index='books',
        body={'settings': {
            'index': {'number_of_shards': 5, 'number_of_routing_shards': 30, 'blocks': {'write': True}}}}
    )
    print("'books' index created!")
    time.sleep(2)  # add sleep to ensure the index has time to become read-only
    client.indices.split(
        index='books',
        target='bigger_books',
        body={'settings': {'index': {'number_of_shards': 10 }}}
    )
    print("'books' index split into 'bigger_books'!")
    client.indices.put_settings(index='books', body={'index': {'blocks': {'write': False}}})
    print("Write operations enabled for 'books' index!")
    
    # Cleanup
    client.indices.delete(index=['movies', 'books', 'movies_clone', 'bigger_books'])
    print("All indices deleted!")




if __name__ == "__main__":
    test_opensearch_examples()