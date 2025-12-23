from typing import Dict, Literal
from eth_typing import ChecksumAddress
from eth_utils.address import to_checksum_address

AddressesType = Literal[
    "SYBEX_ORACLE",
    "SYBEX_BINARY_RESOLVER",
    "SYBEX_CATEGORICAL_RESOLVER",
    "SYBEX_NUMERICAL_RESOLVER",
    "SYBEX_RANGE_NUMERICAL_RESOLVER",
    "SYBEX_AMM",
]

# Addresses: Dict[AddressesType, ChecksumAddress] = {
#     "SYBEX_ORACLE": to_checksum_address("0xf89B35d1f16c6B1Aaf1B78EF2385042C76222237"),
#     "SYBEX_BINARY_RESOLVER": to_checksum_address(
#         "0xB7F72B7Ed6A6Cfb14355bC544a54A68F966B1EEa"
#     ),
#     "SYBEX_CATEGORICAL_RESOLVER": to_checksum_address(
#         "0x794a2f158B7CFc8337FD6E8Cc13E0Ac16c1F7FBd"
#     ),
#     "SYBEX_NUMERICAL_RESOLVER": to_checksum_address(
#         "0xD17fad8923D575414709f7C946280B24b12858b4"
#     ),
#     "SYBEX_RANGE_NUMERICAL_RESOLVER": to_checksum_address(
#         "0xbb944464ba251F4DD1cc460f05BFeEC65F0A3F17"
#     ),
#     "SYBEX_AMM": to_checksum_address("0xE5b4ee5D7041c5ecd485E3b393DC3B6Ff045aBa2"),
# }

Addresses: Dict[AddressesType, ChecksumAddress] = {
    "SYBEX_ORACLE": to_checksum_address("0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"),
    "SYBEX_BINARY_RESOLVER": to_checksum_address(
        "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"
    ),
    "SYBEX_CATEGORICAL_RESOLVER": to_checksum_address(
        "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9"
    ),
    "SYBEX_NUMERICAL_RESOLVER": to_checksum_address(
        "0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9"
    ),
    "SYBEX_RANGE_NUMERICAL_RESOLVER": to_checksum_address(
        "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707"
    ),
    "SYBEX_AMM": to_checksum_address("0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e"),
}