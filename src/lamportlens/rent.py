"""The rent-exempt arithmetic.

Solana requires every account to hold a minimum lamport balance sized to its
data, a bond that is returned in full when the account is closed. The formula
the cluster uses is:

    minimum_balance = (ACCOUNT_STORAGE_OVERHEAD + data_len) * lamports_per_byte

