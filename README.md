<h2 align="center">
Document Embedding Test Structure Using AWS Bedrock
</h2>

<div align="center">
  <img src="https://img.shields.io/badge/python-v3.12.8-blue.svg"/>
  <img src="https://img.shields.io/badge/boto3-v1.35.90-blue.svg"/>
  <img src="https://img.shields.io/badge/opensearch_py-v2.8.0-blue.svg"/>
</div>

이 프로젝트는 문서의 효율적인 검색을 위한 모듈식 테스트 환경입니다. 문서 처리는 다음과 같은 단계로 진행됩니다:

1. 기본 청킹 전략을 통한 문서 분할
2. AWS Bedrock의 Claude를 활용한 Context Retrieval 생성
3. AWS Bedrock의 Titan Embedding으로 벡터 생성
4. 로컬 OpenSearch에 데이터 적재 및 검색 기능 제공

각 단계는 독립적인 모듈로 구성되어 있어, 필요에 따라 다른 전략이나 모델로 확장 가능한 구조를 가지고 있습니다.

---

## 주요 기능

- 다양한 청킹 전략:
  - 고정 크기 청킹
  ~~- 계층적 청킹~~
  ~~- 의미론적 청킹~~
  ~~- 청킹 없음 옵션~~
- AWS Bedrock 통합 (텍스트 임베딩)
- OpenSearch 통합 (문서 저장 및 검색)
- 문맥 검색 지원
- YAML 기반 설정
- 명령줄 인터페이스
- 개별 컴포넌트 테스트 지원

## 필수 요구사항

- AWS Bedrock 접근 권한이 있는 AWS 계정
- Python 3.12.8
- Docker, Docker Compose

---

## 실행 방법

1. 도커 컨테이너 실행 (Opensearch)
```bash
# 컨테이너 실행
docker compose up -d

# 상태 확인
docker ps

# 로그 확인
docker compose logs

# OpenSearch 상태 확인
curl localhost:9200
```

2. AWS 자격 증명 설정
```bash
aws configure
```

3. 실행

```bash
python -m src.cli.main <pdf_file>
```

---

## 모듈별 상세 설명

### 1. Document Processor (document_processor.py)
- **주요 기능**: 문서 로드 및 초기 처리
- **현재 지원**: PDF 파일 형식
- **확장 가능성**:
  - Word, Markdown, HTML 등 다양한 형식 지원 추가 가능
  - 문서 형식별 파서 구현으로 확장

### 2. Chunker (chunker.py)
- **주요 기능**: 문서를 검색 가능한 작은 단위로 분할
- **현재 구현**:
  - 오버랩을 포함한 사이즈 기반 청킹
  - 설정 가능한 청크 크기와 오버랩
- **커스터마이즈 옵션**:
  - 세멘틱 청킹등 구현 가능
  - contextual retrieval로 기본 청킹도 효과적

### 3. Context Generator (context_generator.py)
- **주요 기능**: Claude를 활용한 맥락 정보 생성
- **사용 모델**: Claude 3.5 Haiku
- **작동 방식**:
  1. 문서 캐싱 지원 시:
     - 전체 문서를 캐시에 저장
     - 청크 생성 시 캐시된 전체 문서 참조
     - 별도의 문맥 추출 과정 없이 전체 문서 컨텍스트 활용
  2. 캐싱 미지원 시:
     - 각 청크에 대한 맥락 정보 생성
     - 청크 앞뒤 1000자를 문맥으로 활용
- **최적화 방안**:
  - 문서 크기가 허용하는 경우 전체 문서 캐싱 권장
  - 메모리 효율성과 검색 정확도 향상
  - API 호출 횟수 감소로 비용 절감

### 4. Embedding Models (embedding_models.py)
- **주요 기능**: 텍스트를 벡터로 변환
- **사용 모델**: Amazon Titan Embeddings
- **특징**:
  - 의미적 유사도 계산
  - 빠른 처리 속도

### 5. OpenSearch Client (opensearch_client.py)
- **주요 기능**: OpenSearch 연동 및 검색
- **구현 기능**:
  - 인덱스 생성 및 관리
  - 하이브리드 검색 (BM25 + 벡터 검색)
  - 가중치 기반 결과 통합

---

## 설정

YAML 기반 설정 시스템을 사용합니다. `src/config/default_config.yaml`에 기본 설정이 있으며, 다음 방법으로 설정을 변경할 수 있습니다.

1. 사용자 정의 YAML 파일 생성
2. 명령줄 인수 사용

### AWS Bedrock 설정 예시

```yaml
bedrock:
  region: "us-west-2"
  embedding:
    model_id: "amazon.titan-embed-text-v2:0""
    dimension: 1024
    batch_size: 32
```

## 프로젝트 구조
```
text-embedding-toolkit
├─ LICENSE
├─ README.md
├─ requirements.txt
├─ docker-compose.yml
├─ Dockerfile
├─ sample_data.pdf
└─ src
   ├─ __init__.py
   ├─ cli
   │  ├─ __init__.py
   │  └─ main.py
   ├─ config
   │  ├─ __init__.py
   │  └─ default_config.yaml
   ├─ core
   │  ├─ __init__.py
   │  ├─ chunker.py
   │  ├─ context_generator.py
   │  ├─ document_processor.py
   │  ├─ embedding_models.py
   │  └─ opensearch_client.py
```

## 테스트

```bash
python -m src.cli.main sample_doc.pdf
```

1. **문서 처리 및 임베딩 (Process Document)**
   
   - 메인 메뉴에서 'Process Document' 선택
   - PDF 문서 업로드
   - 청킹, 컨텍스트 생성, 임베딩이 순차적으로 진행
   - OpenSearch에 저장 완료까지 대기
   
   <div align="center">
   <img src="https://github.com/user-attachments/assets/cc29b6ee-853a-4e9b-8698-6c6a8b149452" width="70%">
   </div>
   
2. **문서 검색 테스트 (Search Documents)**
   
   - 임베딩 완료 후 'Search Documents' 선택
   - 검색어 입력하여 결과 확인
   - 하이브리드 검색 결과 (BM25 + 벡터 검색) 표시
   
   <div align="center">
   <img src="https://github.com/user-attachments/assets/4da3c6cb-c090-4f46-81c1-599606b36d52" width="70%">
   </div>
