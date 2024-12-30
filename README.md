# Text Embedding Toolkit

A powerful toolkit for text chunking and semantic search using AWS Bedrock and OpenSearch. This toolkit provides various text chunking strategies and embedding capabilities for efficient document retrieval.

## Features

- AWS Bedrock Integration for text embeddings
- Multiple chunking strategies:
  - Basic Token-based Chunking (300 tokens per chunk)
  - Fixed-size Chunking
  - Hierarchical Chunking
  - Semantic Chunking
  - No Chunking option
- OpenSearch integration for document storage and retrieval
- Contextual retrieval support
- Configurable through YAML
- Command-line interface for easy operation
- Individual component testing capability

## Prerequisites

- AWS Account with Bedrock access
- Python 3.8 or higher
- OpenSearch instance

## Installation

```bash
git clone https://github.com/yourusername/text-embedding-toolkit.git
cd text-embedding-toolkit
pip install -r requirements.txt
```

## Quick Start

1. Configure AWS credentials:
```bash
aws configure
```

2. Set up your configuration in `~/.contextual_retrievalrc` or use the default configuration
3. Run the toolkit:
```bash
python src/main.py
```

4. Follow the interactive prompts to:
   - Select chunking strategy
   - Choose contextual retrieval options
   - Process your documents

## Configuration

The toolkit uses a YAML-based configuration system. Default settings are provided in `src/config/default_config.yaml`. You can override these settings by:

1. Creating a custom YAML file
2. Using command-line arguments
3. Modifying the user config file at `~/.contextual_retrievalrc`

### AWS Bedrock Configuration

```yaml
bedrock:
  region: "us-west-2"
  embedding:
    model_id: "amazon.titan-embed-text-v1"
    dimension: 1536
    batch_size: 10
```

## Testing

Each component includes built-in tests that can be run independently. For example:

```bash
python src/embeddings/embedding_models.py
```

## Chunking Strategies

### Basic Chunking
Splits text into chunks of approximately 300 tokens each. Documents with fewer tokens remain intact.

### Fixed-size Chunking
Divides text into chunks of consistent size based on character count.

### Hierarchical Chunking
Creates a tree structure of chunks with parent-child relationships, allowing for multilevel document representation.

### Semantic Chunking
Groups text based on semantic similarity, ensuring contextually related content stays together.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
text-embedding-toolkit
├─ .DS_Store
├─ .idea
│  ├─ aws.xml
│  ├─ inspectionProfiles
│  │  ├─ Project_Default.xml
│  │  └─ profiles_settings.xml
│  ├─ misc.xml
│  ├─ modules.xml
│  ├─ text-embedding-toolkit.iml
│  ├─ vcs.xml
│  └─ workspace.xml
├─ LICENSE
├─ README.md
└─ src
   ├─ __init__.py
   ├─ __pycache__
   │  ├─ __init__.cpython-312.pyc
   │  ├─ chunker.cpython-312.pyc
   │  ├─ context_generator.cpython-312.pyc
   │  ├─ embedding_models.cpython-312.pyc
   │  └─ opensearch_client.cpython-312.pyc
   ├─ chunker.py
   ├─ config
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  │  └─ __init__.cpython-312.pyc
   │  └─ default_config.yaml
   ├─ context_generator.py
   ├─ document_processor.py
   ├─ embedding_models.py
   ├─ opensearch_client.py
   └─ test_doc.pdf

```
```
text-embedding-toolkit
├─ .DS_Store
├─ .idea
│  ├─ aws.xml
│  ├─ inspectionProfiles
│  │  ├─ Project_Default.xml
│  │  └─ profiles_settings.xml
│  ├─ misc.xml
│  ├─ modules.xml
│  ├─ text-embedding-toolkit.iml
│  ├─ vcs.xml
│  └─ workspace.xml
├─ LICENSE
├─ README.md
└─ src
   ├─ .DS_Store
   ├─ __init__.py
   ├─ __pycache__
   │  └─ __init__.cpython-312.pyc
   ├─ cli
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  │  ├─ __init__.cpython-312.pyc
   │  │  └─ main.cpython-312.pyc
   │  └─ main.py
   ├─ config
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  │  └─ __init__.cpython-312.pyc
   │  └─ default_config.yaml
   ├─ core
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  │  ├─ __init__.cpython-312.pyc
   │  │  ├─ chunker.cpython-312.pyc
   │  │  ├─ context_generator.cpython-312.pyc
   │  │  ├─ document_processor.cpython-312.pyc
   │  │  ├─ embedding_models.cpython-312.pyc
   │  │  └─ opensearch_client.cpython-312.pyc
   │  ├─ chunker.py
   │  ├─ context_generator.py
   │  ├─ document_processor.py
   │  ├─ embedding_models.py
   │  └─ opensearch_client.py
   ├─ knowledge_data_processor.py
   └─ test_doc.pdf

```