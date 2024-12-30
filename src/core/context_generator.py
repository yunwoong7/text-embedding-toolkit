# src/context_generator.py
# Description: Context generator using AWS Bedrock Claude model.

import json
import boto3
from ..config import load_config

_config = load_config()

class ContextGenerator:
    def __init__(self):
        """Initialize context generator with Bedrock client"""
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=_config["bedrock"]["region"]
        )
        self.model_id = _config["bedrock"]["llm"]["model_id"]
        self.max_tokens = _config["bedrock"]["llm"]["max_tokens"]
        self.temperature = _config["bedrock"]["llm"]["temperature"]
        self.context_method = _config["document"]["context_method"]
        self.context_window = _config["document"]["context_window"]
        print(f"Initialized context generator with model={self.model_id}")

    def clean_text(self, text: str) -> str:
        """Clean text by handling encoding issues"""
        return text.encode('utf-8', 'ignore').decode('utf-8')

    def get_context_for_chunk(self, full_doc: str, chunk: str) -> str:
        """Get context for a chunk based on configuration method

        Args:
            full_doc (str): Full document text
            chunk (str): Chunk to get context for

        Returns:
            str: Context for the chunk (full doc or window)
        """
        if self.context_method == "full":
            return full_doc

        # Window method
        chunk_start = full_doc.find(chunk)
        if chunk_start == -1:
            return full_doc

        start = max(0, chunk_start - self.context_window)
        end = min(len(full_doc), chunk_start + len(chunk) + self.context_window)
        return full_doc[start:end]

    def generate_context(self, full_doc: str, chunk: str) -> str:
        """Generate context for a chunk using Bedrock Claude

        Args:
            full_doc (str): Full document content
            chunk (str): The chunk to generate context for

        Returns:
            str: Generated context
        """
        if not full_doc or not chunk:
            raise ValueError("Full document and chunk must not be empty")

        context = self.get_context_for_chunk(full_doc, chunk)

        prompt = f"""Here is a section from a document, with its context:

Document Context:
{context}

Specific Section to Focus on:
{chunk}

Please provide a brief context that situates this specific section within the broader document. Focus on key relationships and relevance.
Answer only with the succinct context, nothing else."""

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [{
                        "role": "user",
                        "content": prompt
                    }],
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                })
            )

            response_body = json.loads(response['body'].read())
            return self.clean_text(response_body['content'][0]['text'])

        except Exception as e:
            raise Exception(f"Error generating context: {str(e)}")


# Test code
if __name__ == "__main__":
    def run_tests():
        print("\n=== Running Context Generator Tests ===\n")

        try:
            # Initialize generator
            print("1. Initializing context generator...")
            generator = ContextGenerator()
            print("   ✓ Generator initialized")

            # Test document
            print("\n2. Testing with sample document...")
            full_doc = """
           1. 개요
           이 문서는 시스템 설계 명세를 담고 있습니다.

           2. 아키텍처
           시스템은 3계층으로 구성됩니다.
           - 프레젠테이션 계층
           - 비즈니스 계층
           - 데이터 계층

           3. 세부사항
           각 계층별 세부 구현사항은 다음과 같습니다.

           3.1 프레젠테이션 계층
           사용자 인터페이스를 담당합니다.

           3.2 비즈니스 계층
           업무 로직을 처리합니다.

           3.3 데이터 계층
           데이터 저장 및 조회를 담당합니다.
           """

            test_chunks = [
                "시스템은 3계층으로 구성됩니다.",
                "비즈니스 계층\n업무 로직을 처리합니다."
            ]

            for i, chunk in enumerate(test_chunks, 1):
                print(f"\nTest chunk #{i}:")
                print(f"Chunk text: '{chunk}'")
                context = generator.generate_context(full_doc, chunk)
                print(f"Generated context: '{context}'")

            # Test error handling
            print("\n3. Testing error handling...")

            print("\nTesting empty input:")
            try:
                generator.generate_context("", "")
                assert False, "Should have failed on empty input"
            except ValueError as e:
                print(f"   ✓ Empty input properly handled: {str(e)}")

            print("\nTesting chunk not in document:")
            context = generator.get_context_for_chunk(full_doc, "이 내용은 문서에 없습니다")
            assert context == full_doc
            print("   ✓ Missing chunk properly handled")

            print("\n✓ All tests passed successfully!")

        except Exception as e:
            print(f"\n✘ Test failed: {str(e)}")
            raise e


    run_tests()