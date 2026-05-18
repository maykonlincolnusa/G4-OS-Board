import pytest


@pytest.mark.integration
def test_rag_retrieval() -> None:
    pytest.skip("Requires running rag-service")
