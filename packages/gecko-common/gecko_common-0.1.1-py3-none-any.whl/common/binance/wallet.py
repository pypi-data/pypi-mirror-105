from binance.client import Client


class Wallet:
    def __init__(self, client: Client):
        self.client = client

    def get_spot_balance(self, asset: str = None) -> dict:
        """
        现货账户余额
        :param asset:
        :return:
        {
            "asset": "KMD",
            "free": "0.00000000",
            "locked": "0.00000000"
        }
        """
        rst = self.client.get_account()
        # list -> dict
        balance = {item['asset']: item for item in rst['balances']}
        if asset:
            return balance[asset.upper()]
        return balance

