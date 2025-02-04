import numpy as np

class InvestmentCalculator:
    def __init__(self):
        self.WEALTHSIMPLE_CURRENCY_CONVERSION = 0.015  # 1.5%
        self.QUESTRADE_CURRENCY_CONVERSION = 0.02  # 2%
        self.QUESTRADE_ECN_FEE = 0.0035  # $0.0035 per share
        self.QUESTRADE_MIN_COMMISSION = 4.95
        self.QUESTRADE_MAX_COMMISSION = 9.95
        self.DLR_COMMISSION = 9.95  # Commission for buying/selling DLR/DLR.U

    def calculate_wealthsimple_costs(self, amount: float, investment_type: str) -> dict:
        conversion_fee = 0
        if investment_type in ["US STOCK", "USD ETF"]:  # Apply conversion fee only to USD investments
            conversion_fee = amount * self.WEALTHSIMPLE_CURRENCY_CONVERSION

        return {
            "platform": "Wealthsimple",
            "conversion_fee": conversion_fee,
            "commission": 0,
            "total_cost": conversion_fee
        }

    def calculate_questrade_regular(self, amount: float, investment_type: str) -> dict:
        conversion_fee = 0
        commission = self.QUESTRADE_MIN_COMMISSION

        if investment_type in ["US STOCK", "USD ETF"]:
            conversion_fee = amount * self.QUESTRADE_CURRENCY_CONVERSION

        # Estimate shares based on approximate price of $50
        estimated_shares = amount / 50
        ecn_fees = estimated_shares * self.QUESTRADE_ECN_FEE

        if investment_type in ["CAD ETF", "USD ETF"]:
            commission = 0  # ETF purchases are free on Questrade

        total_cost = conversion_fee + commission + ecn_fees

        return {
            "platform": "Questrade (Regular)",
            "conversion_fee": conversion_fee,
            "commission": commission,
            "ecn_fees": ecn_fees,
            "total_cost": total_cost
        }

    def calculate_questrade_norberts(self, amount: float, investment_type: str) -> dict:
        if investment_type != "US STOCK":
            return {
                "platform": "Questrade (Norbert's Gambit)",
                "conversion_fee": 0,
                "commission": 0,
                "total_cost": 0,
                "note": "Norbert's Gambit not applicable"
            }

        # Two commissions: one for buying DLR and one for selling DLR.U
        commission = self.DLR_COMMISSION * 2

        # Estimate shares based on approximate DLR price of $13
        estimated_shares = amount / 13
        ecn_fees = estimated_shares * self.QUESTRADE_ECN_FEE * 2  # Two transactions

        total_cost = commission + ecn_fees

        return {
            "platform": "Questrade (Norbert's Gambit)",
            "commission": commission,
            "ecn_fees": ecn_fees,
            "total_cost": total_cost
        }