from mcp.server import MCPServer
from accounts import accounts

mcp = MCPServer("Deepblue Account Manager")

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
    mcp.run()