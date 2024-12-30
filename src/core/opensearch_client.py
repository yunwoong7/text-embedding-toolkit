from typing import List, Dict
from opensearchpy import OpenSearch, helpers
from tqdm import tqdm
from ..config import load_config

class OpenSearchHandler:
    def __init__(self):
        config = load_config()
        self.config = config["opensearch"]
        self.client = self._init_client()
        self.index_name = self.config["common"]["index_name"]
        self.bulk_size = self.config["common"]["bulk_size"]
        self.embedding_dim = config["bedrock"]["embedding"]["dimension"]

    def _init_client(self) -> OpenSearch:
        if self.config["mode"] == "local":
            return OpenSearch(
                hosts=[{
                    'host': self.config["local"]["host"],
                    'port': self.config["local"]["port"]
                }],
                http_compress=True,
                use_ssl=False,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False
            )
        else:
            import boto3
            from opensearchpy import RequestsHttpConnection
            from requests_aws4auth import AWS4Auth

            credentials = boto3.Session().get_credentials()
            auth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                self.config["aws"]["region"],
                'es',
                session_token=credentials.token
            )

            return OpenSearch(
                hosts=[{
                    'host': self.config["aws"]["host"],
                    'port': self.config["aws"]["port"]
                }],
                http_compress=True,
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                pool_maxsize=20
            )

    def create_index(self, recreate: bool = False):
        if recreate and self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)

        if not self.client.indices.exists(index=self.index_name):
            index_body = {
                "settings": {
                    "index": {
                        "knn": True
                    },
                    "analysis": {
                        "analyzer": {
                            "nori_analyzer": {
                                "type": "custom",
                                "tokenizer": "nori_tokenizer",
                                "filter": ["nori_number", "nori_readingform", "lowercase"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "content": {
                            "type": "text",
                            "analyzer": "nori_analyzer"
                        },
                        "context": {
                            "type": "text",
                            "analyzer": "nori_analyzer"
                        },
                        "content_vector": {
                            "type": "knn_vector",
                            "dimension": self.embedding_dim,
                            "method": {
                                "name": "hnsw",
                                "space_type": "cosinesimil",
                                "engine": "nmslib"
                            }
                        }
                    }
                }
            }

            self.client.indices.create(
                index=self.index_name,
                body=index_body
            )

            pipeline_body = {
                "description": "Knowledge search hybrid pipeline",
                "phase_results_processors": [
                    {
                        "normalization-processor": {
                            "normalization": {
                                "technique": "min_max"
                            },
                            "combination": {
                                "technique": "arithmetic_mean",
                                "parameters": {
                                    "weights": [0.3, 0.7]
                                }
                            }
                        }
                    }
                ]
            }

            try:
                self.client.transport.perform_request(
                    'PUT',
                    '/_search/pipeline/contextual-search-pipeline',
                    body=pipeline_body
                )
            except Exception as e:
                print(f"Error creating search pipeline: {str(e)}")

    def index_documents(self,
                        chunks: List[str],
                        raw_text: str,
                        context_generator,
                        embedding_model) -> None:
        docs = []
        for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
            context = context_generator.generate_context(raw_text, chunk)
            combined_text = f"내용: {chunk}\n맥락: {context}"
            embedding = embedding_model.encode_single(combined_text)
            doc = {
                "_index": self.index_name,
                "_id": str(i),
                "content": chunk.strip(),
                "context": context.strip(),
                "content_vector": embedding.tolist()
            }
            docs.append(doc)

        for i in range(0, len(docs), self.bulk_size):
            chunk_docs = docs[i:i + self.bulk_size]
            try:
                helpers.bulk(self.client, chunk_docs, max_retries=3)
            except Exception as e:
                print(f"Error indexing chunk {i}-{i + len(chunk_docs)}: {str(e)}")

    def search(self, query: str, embedding_model, k: int = 5) -> List[Dict]:
        combined_query = f"질문: {query}\n맥락: {query}"
        query_vector = embedding_model.encode_single(combined_query).tolist()

        search_body = {
            "size": k,
            "query": {
                "hybrid": {
                    "queries": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["content"],
                                "analyzer": "nori_analyzer",
                                "type": "best_fields",
                                "tie_breaker": 0.3
                            }
                        },
                        {
                            "knn": {
                                "content_vector": {
                                    "vector": query_vector,
                                    "k": k
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [{"_score": "desc"}]
        }

        response = self.client.search(
            index=self.index_name,
            body=search_body,
            params={"search_pipeline": "contextual-search-pipeline"}
        )

        results = []
        for hit in response['hits']['hits']:
            results.append({
                'content': hit['_source']['content'],
                'context': hit['_source']['context'],
                'score': hit['_score']
            })
        return results
