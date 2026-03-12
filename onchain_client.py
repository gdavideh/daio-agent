from web3 import Web3
from eth_account import Account
import os
import json

class OnChainClient:
    def __init__(self, private_key=None, rpc_url=None):
        self.rpc_url = rpc_url or os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.private_key = private_key or os.getenv("AGENT_PRIVATE_KEY")
        if self.private_key:
            self.account = Account.from_key(self.private_key)
        else:
            self.account = None

        # DAIO DAO Baal v3 Contract Address on Base
        self.dao_address = os.getenv("DAIO_DAO_ADDRESS", "0x0000000000000000000000000000000000000000")
        self.identity_registry = os.getenv("IDENTITY_REGISTRY_ADDRESS", "0x0000000000000000000000000000000000000000")

    def submit_dao_proposal(self, multicall_data, description, expiration=0):
        """
        Submits a proposal to the Baal (MolochV3) DAO.
        multicall_data: ABI-encoded bytes of the actions to perform.
        description: String description of the proposal.
        expiration: Timestamp when the proposal expires (0 for none).
        """
        if not self.account:
            return "Error: No account configured."

        # Baal v3 submitProposal ABI
        abi = [{
            "inputs": [
                {"internalType": "bytes", "name": "proposalData", "type": "bytes"},
                {"internalType": "uint32", "name": "expiration", "type": "uint32"},
                {"internalType": "string", "name": "details", "type": "string"}
            ],
            "name": "submitProposal",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function"
        }]

        contract = self.w3.eth.contract(address=self.dao_address, abi=abi)
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        tx = contract.functions.submitProposal(
            multicall_data, 
            expiration, 
            description
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def vote_on_proposal(self, proposal_id, support):
        """
        Votes on an active proposal.
        proposal_id: The ID of the proposal.
        support: Boolean (True for Yes, False for No).
        """
        if not self.account:
            return "Error: No account configured."

        # Baal v3 submitVote ABI
        abi = [{
            "inputs": [
                {"internalType": "uint32", "name": "proposalId", "type": "uint32"},
                {"internalType": "bool", "name": "approved", "type": "bool"}
            ],
            "name": "submitVote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }]

        contract = self.w3.eth.contract(address=self.dao_address, abi=abi)
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        tx = contract.functions.submitVote(
            int(proposal_id), 
            support
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

if __name__ == "__main__":
    # Example usage
    client = OnChainClient()
    print(f"Connected: {client.w3.is_connected()}")
    if client.account:
        print(f"Address: {client.account.address}")
