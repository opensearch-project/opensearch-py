clean:
	docker-compose down --remove-orphans --volumes

build:
	PYTHON_VERSION=${PYTHON_VERSION} docker-compose build client

pull:
	OPENSEARCH_VERSION=${OPENSEARCH_VERSION} PYTHON_VERSION=${PYTHON_VERSION} docker-compose pull

push:
	# requires authentication.
	PYTHON_VERSION=${PYTHON_VERSION} docker-compose push client

run_tests:
	OPENSEARCH_VERSION=${OPENSEARCH_VERSION} PYTHON_VERSION=${PYTHON_VERSION} docker-compose -p "${OPEN_VERSION}-${PYTHON_VERSION}" run client python test_opensearchpy/run_tests.py

start_opensearch:
	OPENSEARCH_VERSION=${OPENSEARCH_VERSION} docker-compose up -d opensearch
