import uuid
import random
import json
from src.ipfs import IPFSClient
from src.relayer.client import RelayerClient
from src.proof import generate_proof

client = RelayerClient()
ipfs = IPFSClient()


def resolve_question():
    question_id = random.randint(0, 19)
    outcome = random.randint(0, 1)

    proof_data = f"Proof for {question_id} with outcome {outcome}"

    proof_params = generate_proof(
        question_id=question_id, outcome=outcome, proof_data=proof_data
    )

    proof_id = str(uuid.uuid4())

    ipfs_response = ipfs.write(filename=f"{proof_id}.json", data=json.dumps(proof_params))

    print(ipfs_response)


if __name__ == "__main__":
    resolve_question()
