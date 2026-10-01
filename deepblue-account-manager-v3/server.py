from mcp.server import MCPServer
from accounts import accounts

mcp = MCPServer("Deepblue Account Manager REMOTE V3")

####################################################
# Resources 
####################################################
@mcp.resource("deepblue://accounts/account-creation-policy")
def account_creation_policy() -> str:
    """
    Returns the account creation policy. The new account creation procedure must adhere to it
    """
    return """Maximum 5 total accounts should exist, not more than that . 
    Duplicate account name should not be created. 
    Initial Balance of account should be greater than 1000 USD. """

####################################################
# Resource Template
####################################################
@mcp.resource("deepblue://accounts/{accountId}/transaction-history")
def account_history(accountId: str) -> str:
    """
    Returns the historical data for a specific account Id.
    """
    account = accounts.get(accountId)

    if account is None:
        return f"Account '{accountId}' does not exist."

    # For demonstration purposes, we'll return a static transaction history.
    # In a real application, this would likely query a database or another data source.
    transaction_history = [
        {"date": "2026-01-01", "type": "deposit", "amount": 500},
        {"date": "2026-02-15", "type": "withdrawal", "amount": 200},
        {"date": "2026-03-10", "type": "deposit", "amount": 300},
    ]

    return f"Transaction history for account '{accountId}': {transaction_history}"

####################################################
# Prompts
####################################################
@mcp.prompt()
def account_creation_sample_prompt(name: str, email: str, initial_balance: float) -> str:
    """
    Returns a prompt for creating a new account.
    """
    return f"Please create a new account for {name} with email {email} and initial balance ${initial_balance:.2f}."

@mcp.prompt()
def filter_accounts_sample_prompt(balance: float) -> str:
    """
    Prompt for filtering accounts by balance.
    """
    return f"Please filter accounts with less than ${balance:.2f}."

####################################################
# LIST ACCOUNTS
####################################################

@mcp.tool()
def list_accounts() -> dict:
    """
    Return all customer accounts
    """
    return { 
        "success": True,
        "count": len(accounts),
        "accounts": list(accounts.values())
    }

###################################################
# GET ACCOUNT
####################################################
@mcp.tool()
def get_account(accountId: str) -> dict:
    """
    Returns an account by Account Id.
    """

    account = accounts.get(accountId)

    if account is None:
        return {
            "success": False,
            "message": f"Account '{accountId}' does not exist."
        }

    return {
        "success": True,
        "account": account
    }


####################################################
# ADD ACCOUNT
####################################################
@mcp.tool()
def add_account(
        accountId: str,
        name: str,
        email: str,
        balance: float = 0
) -> dict:
    """
    Adds a new customer account.
    """

    if accountId in accounts:
        return {
            "success": False,
            "message": f"Account '{accountId}' already exists."
        }

    accounts[accountId] = {
        "accountId": accountId,
        "name": name,
        "email": email,
        "balance": balance
    }

    return {
        "success": True,
        "message": "Account created successfully.",
        "account": accounts[accountId]
    }


####################################################
# UPDATE ACCOUNT
####################################################
@mcp.tool()
def update_account(
        accountId: str,
        name: str = None,
        email: str = None,
        balance: float = None
) -> dict:
    """
    Updates an existing account.
    """

    account = accounts.get(accountId)

    if account is None:
        return {
            "success": False,
            "message": f"Account '{accountId}' does not exist."
        }

    if name is not None:
        account["name"] = name

    if email is not None:
        account["email"] = email

    if balance is not None:
        account["balance"] = balance

    return {
        "success": True,
        "message": "Account updated successfully.",
        "account": account
    }


####################################################
# DELETE ACCOUNT
####################################################
@mcp.tool()
def delete_account(accountId: str) -> dict:
    """
    Deletes an account.
    """

    account = accounts.get(accountId)

    if account is None:
        return {
            "success": False,
            "message": f"Account '{accountId}' does not exist."
        }

    deleted = accounts.pop(accountId)

    return {
        "success": True,
        "message": "Account deleted successfully.",
        "deletedAccount": deleted
    }



if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=5001)