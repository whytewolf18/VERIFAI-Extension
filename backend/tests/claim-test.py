import pytest
from utils.claim_detector import detect_claim

def test_detect_claim():
    assert detect_claim("The president claims that the economy is growing.") == True
    assert detect_claim("It is true that the new policy will benefit everyone.") == True
    assert detect_claim("This is a simple statement without any claim.") == False
    assert detect_claim("Experts say that this is the best solution.") == True
    assert detect_claim("No claim here.") == False

if __name__ == "__main__":
    pytest.main()