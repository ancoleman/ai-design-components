# Elasticsearch Integration Patterns

## Python Elasticsearch Client Setup

### Basic Connection
```python
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging

logger = logging.getLogger(__name__)

class ElasticsearchClient:
    """Elasticsearch client wrapper with connection management."""

    def __init__(self, hosts=['localhost:9200'], **kwargs):
        """Initialize Elasticsearch connection."""
        self.es = Elasticsearch(
            hosts=hosts,
            # Authentication if needed
            http_auth=kwargs.get('http_auth'),
            # Connection parameters
            timeout=kwargs.get('timeout', 30),
            max_retries=kwargs.get('max_retries', 3),
            retry_on_timeout=kwargs.get('retry_on_timeout', True)
        )

        # Verify connection
        if not self.es.ping():
            raise ValueError("Connection to Elasticsearch failed")

        logger.info(f"Connected to Elasticsearch: {self.es.info()['version']['number']}")

    def create_index(self, index_name: str, mappings: dict, settings: dict = None):
        """Create an index with mappings."""
        body = {}

        if settings:
            body['settings'] = settings

        if mappings:
            body['mappings'] = mappings

        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=body)
            logger.info(f"Created index: {index_name}")
        else:
            logger.info(f"Index {index_name} already exists")

    def delete_index(self, index_name: str):
        """Delete an index."""
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
            logger.info(f"Deleted index: {index_name}")
```

## Index Design and Mappings

### Product Search Index
```python
class ProductIndexManager:
    """Manage product search index."""

    PRODUCT_INDEX = 'products'

    PRODUCT_MAPPING = {
        'properties': {
            'id': {'type': 'keyword'},
            'title': {
                'type': 'text',
                'analyzer': 'standard',
                'fields': {
                    'keyword': {'type': 'keyword'},
                    'suggest': {
                        'type': 'search_as_you_type'
                    }
                }
            },
            'description': {
                'type': 'text',
                'analyzer': 'english'
            },
            'category': {
                'type': 'keyword',
                'fields': {
                    'text': {'type': 'text'}
                }
            },
            'brand': {'type': 'keyword'},
            'price': {'type': 'float'},
            'tags': {'type': 'keyword'},
            'in_stock': {'type': 'boolean'},
            'created_at': {'type': 'date'},
            'rating': {'type': 'float'},
            'review_count': {'type': 'integer'},
            'image_url': {'type': 'keyword'},
            'attributes': {
                'type': 'nested',
                'properties': {
                    'name': {'type': 'keyword'},
                    'value': {'type': 'keyword'}
                }
            }
        }
    }

    INDEX_SETTINGS = {
        'number_of_shards': 1,
        'number_of_replicas': 1,
        'analysis': {
            'analyzer': {
                'autocomplete': {
                    'tokenizer': 'autocomplete',
                    'filter': ['lowercase']
                },
                'autocomplete_search': {
                    'tokenizer': 'lowercase'
                }
            },
            'tokenizer': {
                'autocomplete': {
                    'type': 'edge_ngram',
                    'min_gram': 2,
                    'max_gram': 10,
                    'token_chars': ['letter', 'digit']
                }
            }
        }
    }

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es

    def create_product_index(self):
        """Create product index with optimized mappings."""
        self.es_client.create_index(
            self.PRODUCT_INDEX,
            self.PRODUCT_MAPPING,
            self.INDEX_SETTINGS
        )

    def index_products(self, products: list):
        """Bulk index products."""
        actions = []

        for product in products:
            action = {
                '_index': self.PRODUCT_INDEX,
                '_id': product['id'],
                '_source': product
            }
            actions.append(action)

        success, failed = bulk(self.es, actions, raise_on_error=False)
        logger.info(f"Indexed {success} products, {len(failed)} failed")

        if failed:
            logger.error(f"Failed to index: {failed}")

        return success, failed
```

## Search Query Patterns

### Full-Text Search with Filters
```python
from typing import Dict, List, Optional, Any

class ProductSearcher:
    """Execute product searches with Elasticsearch."""

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es

    def search(
        self,
        query: str = None,
        filters: Dict[str, Any] = None,
        sort_by: str = None,
        page: int = 1,
        size: int = 20,
        facets: List[str] = None
    ):
        """Perform product search with filters and facets."""

        # Build Elasticsearch query
        es_query = self._build_query(query, filters)

        # Build request body
        body = {
            'query': es_query,
            'from': (page - 1) * size,
            'size': size
        }

        # Add sorting
        if sort_by:
            body['sort'] = self._build_sort(sort_by)

        # Add aggregations for facets
        if facets:
            body['aggs'] = self._build_aggregations(facets)

        # Execute search
        response = self.es.search(
            index='products',
            body=body
        )

        return self._parse_response(response)

    def _build_query(self, query: str, filters: Dict[str, Any]):
        """Build Elasticsearch query with filters."""
        must = []
        filter_clauses = []

        # Text search
        if query:
            must.append({
                'multi_match': {
                    'query': query,
                    'fields': [
                        'title^3',      # Boost title matches
                        'description^2',  # Medium boost for description
                        'tags',
                        'category.text',
                        'brand'
                    ],
                    'type': 'best_fields',
                    'fuzziness': 'AUTO'
                }
            })

        # Apply filters
        if filters:
            for field, value in filters.items():
                if isinstance(value, list):
                    # Multiple values - use terms query
                    filter_clauses.append({
                        'terms': {field: value}
                    })
                elif isinstance(value, dict):
                    # Range filter
                    if 'min' in value or 'max' in value:
                        range_filter = {}
                        if 'min' in value:
                            range_filter['gte'] = value['min']
                        if 'max' in value:
                            range_filter['lte'] = value['max']

                        filter_clauses.append({
                            'range': {field: range_filter}
                        })
                else:
                    # Exact match
                    filter_clauses.append({
                        'term': {field: value}
                    })

        # Combine queries
        if must or filter_clauses:
            return {
                'bool': {
                    'must': must,
                    'filter': filter_clauses
                }
            }
        else:
            return {'match_all': {}}

    def _build_sort(self, sort_by: str):
        """Build sort clause."""
        sort_options = {
            'relevance': ['_score'],
            'price_asc': [{'price': 'asc'}],
            'price_desc': [{'price': 'desc'}],
            'newest': [{'created_at': 'desc'}],
            'rating': [{'rating': 'desc'}],
        }

        return sort_options.get(sort_by, ['_score'])

    def _build_aggregations(self, facets: List[str]):
        """Build aggregations for faceted search."""
        aggs = {}

        for facet in facets:
            if facet == 'price':
                # Range aggregation for price
                aggs['price_ranges'] = {
                    'range': {
                        'field': 'price',
                        'ranges': [
                            {'key': 'Under $50', 'to': 50},
                            {'key': '$50-$100', 'from': 50, 'to': 100},
                            {'key': '$100-$200', 'from': 100, 'to': 200},
                            {'key': 'Over $200', 'from': 200}
                        ]
                    }
                }
            else:
                # Terms aggregation for categorical fields
                aggs[facet] = {
                    'terms': {
                        'field': facet,
                        'size': 20
                    }
                }

        return aggs

    def _parse_response(self, response):
        """Parse Elasticsearch response."""
        results = {
            'total': response['hits']['total']['value'],
            'items': [],
            'facets': {}
        }

        # Extract search results
        for hit in response['hits']['hits']:
            item = hit['_source']
            item['_score'] = hit['_score']
            results['items'].append(item)

        # Extract facets
        if 'aggregations' in response:
            for facet_name, facet_data in response['aggregations'].items():
                if 'buckets' in facet_data:
                    results['facets'][facet_name] = [
                        {
                            'value': bucket.get('key'),
                            'count': bucket.get('doc_count')
                        }
                        for bucket in facet_data['buckets']
                    ]

        return results
```

### Autocomplete/Suggestions
```python
class AutocompleteSearcher:
    """Implement autocomplete with Elasticsearch."""

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es

    def suggest(self, prefix: str, size: int = 10):
        """Get autocomplete suggestions."""
        body = {
            'query': {
                'multi_match': {
                    'query': prefix,
                    'type': 'bool_prefix',
                    'fields': [
                        'title.suggest',
                        'title.suggest._2gram',
                        'title.suggest._3gram'
                    ]
                }
            },
            'size': size,
            '_source': ['title', 'category', 'brand']
        }

        response = self.es.search(index='products', body=body)

        suggestions = []
        for hit in response['hits']['hits']:
            suggestions.append({
                'text': hit['_source']['title'],
                'category': hit['_source'].get('category'),
                'brand': hit['_source'].get('brand')
            })

        return suggestions

    def search_as_you_type(self, query: str):
        """Real-time search suggestions."""
        body = {
            'suggest': {
                'product-suggest': {
                    'prefix': query,
                    'completion': {
                        'field': 'title.suggest',
                        'size': 5,
                        'skip_duplicates': True
                    }
                }
            }
        }

        response = self.es.search(index='products', body=body)

        suggestions = []
        for option in response['suggest']['product-suggest'][0]['options']:
            suggestions.append({
                'text': option['text'],
                'score': option['_score']
            })

        return suggestions
```

## Advanced Search Features

### Boolean Query Builder
```python
class BooleanQueryBuilder:
    """Build complex boolean queries for Elasticsearch."""

    def build_advanced_query(self, search_params: Dict):
        """
        Build advanced query with AND/OR/NOT operators.

        Example params:
        {
            'must': ['laptop', 'dell'],
            'should': ['gaming', 'professional'],
            'must_not': ['refurbished'],
            'fields': {
                'title': 'laptop',
                'brand': 'dell'
            }
        }
        """
        bool_query = {
            'bool': {}
        }

        # Must clauses (AND)
        if 'must' in search_params:
            bool_query['bool']['must'] = [
                {'match': {'_all': term}}
                for term in search_params['must']
            ]

        # Should clauses (OR)
        if 'should' in search_params:
            bool_query['bool']['should'] = [
                {'match': {'_all': term}}
                for term in search_params['should']
            ]
            bool_query['bool']['minimum_should_match'] = 1

        # Must not clauses (NOT)
        if 'must_not' in search_params:
            bool_query['bool']['must_not'] = [
                {'match': {'_all': term}}
                for term in search_params['must_not']
            ]

        # Field-specific searches
        if 'fields' in search_params:
            if 'must' not in bool_query['bool']:
                bool_query['bool']['must'] = []

            for field, value in search_params['fields'].items():
                bool_query['bool']['must'].append({
                    'match': {field: value}
                })

        return bool_query
```

### Relevance Tuning
```python
class RelevanceTuner:
    """Tune search relevance with boosting and scoring."""

    def search_with_boosting(self, query: str, user_context: Dict = None):
        """Search with context-aware boosting."""

        # Base query
        base_query = {
            'multi_match': {
                'query': query,
                'fields': [
                    'title^3',
                    'description^2',
                    'tags'
                ]
            }
        }

        # Apply function score for personalization
        function_score = {
            'function_score': {
                'query': base_query,
                'functions': []
            }
        }

        # Boost recent products
        function_score['function_score']['functions'].append({
            'gauss': {
                'created_at': {
                    'origin': 'now',
                    'scale': '30d',
                    'decay': 0.5
                }
            },
            'weight': 1.5
        })

        # Boost highly rated products
        function_score['function_score']['functions'].append({
            'field_value_factor': {
                'field': 'rating',
                'factor': 1.2,
                'modifier': 'sqrt',
                'missing': 1
            }
        })

        # User preference boosting
        if user_context and 'preferred_categories' in user_context:
            for category in user_context['preferred_categories']:
                function_score['function_score']['functions'].append({
                    'filter': {'term': {'category': category}},
                    'weight': 2.0
                })

        # Combine scores
        function_score['function_score']['score_mode'] = 'sum'
        function_score['function_score']['boost_mode'] = 'multiply'

        return function_score
```

## Performance Optimization

### Query Caching
```python
from functools import lru_cache
import hashlib
import json

class ElasticsearchCache:
    """Cache Elasticsearch queries for performance."""

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es
        self._cache = {}

    @lru_cache(maxsize=100)
    def _get_cache_key(self, query_str: str):
        """Generate cache key from query."""
        return hashlib.md5(query_str.encode()).hexdigest()

    def search_with_cache(self, index: str, body: dict, cache_ttl: int = 300):
        """Execute search with caching."""

        # Generate cache key
        query_str = json.dumps(body, sort_keys=True)
        cache_key = self._get_cache_key(query_str)

        # Check cache
        if cache_key in self._cache:
            cached_result, timestamp = self._cache[cache_key]
            if time.time() - timestamp < cache_ttl:
                return cached_result

        # Execute query
        result = self.es.search(index=index, body=body)

        # Cache result
        self._cache[cache_key] = (result, time.time())

        return result
```

### Scroll API for Large Results
```python
class ScrollSearcher:
    """Handle large result sets with scroll API."""

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es

    def scroll_all_products(self, query: dict = None, batch_size: int = 1000):
        """Scroll through all matching products."""

        if query is None:
            query = {'match_all': {}}

        # Initialize scroll
        response = self.es.search(
            index='products',
            body={'query': query, 'size': batch_size},
            scroll='2m'  # Keep scroll context for 2 minutes
        )

        scroll_id = response['_scroll_id']
        results = response['hits']['hits']

        # Yield first batch
        yield results

        # Continue scrolling
        while len(results) > 0:
            response = self.es.scroll(
                scroll_id=scroll_id,
                scroll='2m'
            )

            scroll_id = response['_scroll_id']
            results = response['hits']['hits']

            if results:
                yield results

        # Clear scroll context
        self.es.clear_scroll(scroll_id=scroll_id)
```

## Index Management

### Reindexing Strategy
```python
class IndexManager:
    """Manage index lifecycle and reindexing."""

    def reindex_with_zero_downtime(self, old_index: str, new_index: str, new_mapping: dict):
        """Reindex with zero downtime using aliases."""

        # 1. Create new index with updated mapping
        self.es.indices.create(index=new_index, body={'mappings': new_mapping})

        # 2. Reindex data
        self.es.reindex(
            body={
                'source': {'index': old_index},
                'dest': {'index': new_index}
            },
            wait_for_completion=False
        )

        # 3. Wait for reindex to complete
        task_id = response['task']
        self._wait_for_task(task_id)

        # 4. Verify document count
        old_count = self.es.count(index=old_index)['count']
        new_count = self.es.count(index=new_index)['count']

        if old_count != new_count:
            raise ValueError(f"Document count mismatch: {old_count} vs {new_count}")

        # 5. Switch alias atomically
        self.es.indices.update_aliases(
            body={
                'actions': [
                    {'remove': {'index': old_index, 'alias': 'products'}},
                    {'add': {'index': new_index, 'alias': 'products'}}
                ]
            }
        )

        # 6. Delete old index (optional)
        # self.es.indices.delete(index=old_index)

        logger.info(f"Successfully reindexed from {old_index} to {new_index}")
```

## Error Handling

### Robust Search with Retries
```python
from elasticsearch.exceptions import (
    ConnectionError,
    ConnectionTimeout,
    TransportError
)
import time

class RobustSearcher:
    """Elasticsearch search with error handling and retries."""

    def __init__(self, es_client: ElasticsearchClient):
        self.es = es_client.es
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def search_with_retry(self, index: str, body: dict):
        """Execute search with automatic retry on failure."""

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return self.es.search(index=index, body=body)

            except ConnectionTimeout as e:
                logger.warning(f"Search timeout (attempt {attempt + 1}): {e}")
                last_exception = e
                time.sleep(self.retry_delay * (attempt + 1))

            except ConnectionError as e:
                logger.error(f"Connection error (attempt {attempt + 1}): {e}")
                last_exception = e
                time.sleep(self.retry_delay * (attempt + 1))

            except TransportError as e:
                if e.status_code == 429:  # Too many requests
                    logger.warning(f"Rate limited, backing off...")
                    time.sleep(self.retry_delay * (attempt + 2))
                else:
                    logger.error(f"Transport error: {e}")
                    raise

        # All retries failed
        raise last_exception
```