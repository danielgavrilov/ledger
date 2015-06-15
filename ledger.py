from collections import defaultdict
import datetime
import csv

class Column:
    Date, Payer, Payee, Amount = range(4)

class Ledger:

    @classmethod
    def from_file(self, filename):
        with open(filename, 'rb') as csvfile:
            transactions = list(csv.reader(csvfile))
        return Ledger(transactions)

    @staticmethod
    def parse_date(datestring):
        return datetime.datetime.strptime(datestring, '%Y-%m-%d')

    def __init__(self, transactions):
        self.transactions = transactions
    
    def get_transactions(self, before=None):
        if before is None: return self.transactions
        date = self.parse_date(before)
        earlier_than_date = lambda row: self.parse_date(row[Column.Date]) < date
        return filter(earlier_than_date, self.transactions)

    def get_all_balances(self, before=None):
        transactions = self.get_transactions(before)
        # defaultdict returns default value (0.00) when key doesn't exist
        entities = defaultdict(float)

        for row in transactions:
            payer  = row[Column.Payer]
            payee  = row[Column.Payee]
            amount = float(row[Column.Amount])
            entities[payer] -= amount
            entities[payee] += amount

        return entities

    def get_balance(self, entity, before=None):
        return self.get_all_balances(before=before)[entity]


# I would probably use a test framework and more extensive tests if this was
# going into production. But this is simple and easy.
def test():

    ledger = Ledger.from_file('test.csv')

    # correctly initialized
    assert ledger.get_all_balances(before='2015-01-16') == {}
    assert ledger.get_balance('mary', before='2015-01-16') == 0

    # single transfer
    assert ledger.get_balance('mary', before='2015-01-17') == 125.00
    assert ledger.get_balance('john', before='2015-01-17') == -125.00

    # final balance
    assert ledger.get_balance('john') == -145.01
    assert ledger.get_balance('paypal') == 0.01

    print('All tests pass.')
    
    
