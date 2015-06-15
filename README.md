# Usage

The easiest way to use this is in interactive mode: 

```bash
python -i ledger.py
```

Once in interactive mode, you can create an instance from a csv file: 

```python
ledger = Ledger.from_file('test.csv')

# get a dictionary with the balances for all entities
ledger.get_all_balances(before='2015-01-17')

# get the balance for a specific entity
ledger.get_balance('mary', before='2015-01-17')

# In both cases, the `before` argument is optional. Not supplying it considers
# every transaction made.
```
