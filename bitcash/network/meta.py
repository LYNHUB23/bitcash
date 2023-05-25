TX_TRUST_LOW = 1
TX_TRUST_MEDIUM = 6
TX_TRUST_HIGH = 30


class Unspent:
    """
    Represents an unspent transaction output (UTXO) with CashToken
    """

    __slots__ = ("amount", "confirmations", "script", "txid",
                 "txindex", "catagory_id", "nft_capability", "nft_commitment",
                 "token_amount")

    NFT_CAPABILITY = ["none", "mutable", "minting"]

    def __init__(
        self,
        amount,
        confirmations,
        script,
        txid,
        txindex,
        catagory_id=None,
        nft_capability=None,
        nft_commitment=None,
        token_amount=None
    ):
        self.amount = amount
        self.confirmations = confirmations
        self.script = script
        self.txid = txid
        self.txindex = txindex
        self.catagory_id = catagory_id
        self.nft_capability = nft_capability
        self.nft_commitment = nft_commitment
        self.token_amount = token_amount

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in Unspent.__slots__}

    @classmethod
    def from_dict(cls, d):
        return Unspent(**{attr: d[attr] for attr in Unspent.__slots__})

    @property
    def has_nft(self):
        return self.nft_capability is not None

    @property
    def has_amount(self):
        return self.token_amount is not None

    @property
    def has_cashtoken(self):
        return self.has_amount or self.has_nft

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __gt__(self, other):
        """
        Method to help sorting of Unspents during spending
        """
        if self.has_nft:
            if not other.has_nft:
                return True
            if (
                Unspent.NFT_CAPABILITY.index(self.nft_capability)
                > Unspent.NFT_CAPABILITY.index(other.nft_capability)
            ):
                return True
            if (
                Unspent.NFT_CAPABILITY.index(self.nft_capability)
                < Unspent.NFT_CAPABILITY.index(other.nft_capability)
            ):
                return False
        elif other.has_nft:
            return False
        if self.has_amount:
            if not other.has_amount:
                return True
            if (self.token_amount > other.token_amount):
                return True
            if (self.token_amount < other.token_amount):
                return False
        elif other.has_amount:
            return False
        return self.amount > other.amount

    def __repr__(self):

        var_list = [f"{key}={repr(value)}"
                    for key, value in self.to_dict().items()
                    if value is not None]
        return "Unspent({})".format(", ".join(var_list))
