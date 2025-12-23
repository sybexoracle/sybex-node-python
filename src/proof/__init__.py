def generate_proof(question_id: int, outcome: int, proof_data: str) -> dict:
    params = {
        "question_id": question_id,
        "outcome": outcome,
        "proof_data": proof_data,
    }

    return params
