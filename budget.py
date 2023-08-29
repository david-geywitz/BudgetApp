def get_withdrawal(category):
    withdrawal = 0
    for activities in category.ledger:
        if activities['amount'] < 0 and 'Transfer' not in activities['description']:
            withdrawal += activities['amount']
        else:
            continue
    return withdrawal

def create_spend_chart(categories):
    total_withdrawal = 0
    for category in categories:
        for activities in category.ledger:
            if activities['amount'] < 0 and 'Transfer' not in activities['description']:
                total_withdrawal += activities['amount']
            else:
                continue
    title = 'Percentage spent by category'
    percentage = 100
    graph = []
    row = str(percentage) + '|' + ' '
    while percentage >= 0:
        for category in categories:
            if get_withdrawal(category)/total_withdrawal * 100 >= percentage:
                row = row + 'o' + '  '
            else:
                row = row + '   '
        percentage -= 10
        graph.append(row)
        row = str(percentage).rjust(3) + '|' + ' '

    dasher = '    ' + '-' * (len(categories) * 3 + 1) + '\n'
    longest_sentence = 0
    for category in categories:
        if longest_sentence == 0:
            longest_sentence = len(category.name)
        elif len(category.name) > longest_sentence:
            longest_sentence = len(category.name)
        else:
            continue
    x = 0
    i = 0
    line = '     '
    while x < longest_sentence:
        while i < longest_sentence:
            for category in categories:
                try:
                    line = line + category.name[i] + '  '
                except IndexError:
                    line = line + '   '
            i += 1
            if i < longest_sentence:
                line = line + '\n' + '     '
        x += 1

    return title + '\n' + '\n'.join(graph) + '\n' + dasher + line


class Category:

    def __init__(self, category):
        self.name = category
        self.ledger = []

    def __str__(self):
        display = ['{}'.format(self.name).center(30, '*')]
        for elements in self.ledger:
            if len(elements['description']) > 23:
                elements['description'] = elements['description'][:23]
            display.append(str(elements['description']).ljust(23) + '{:.2f}'.format(float(elements['amount'])).rjust(7))
        display.append('Total: {}'.format(float(self.get_balance())))
        return '\n'.join(display)

    def get_balance(self):
        total_balance = 0
        for balance in self.ledger:
            total_balance += balance['amount']
        return total_balance

    def check_funds(self, amount):
        total_balance = self.get_balance()
        if total_balance >= amount:
            return True
        else:
            return False

    def deposit(self, amount, description=''):
        _deposit = {'amount': amount, 'description': description}
        self.ledger.append(_deposit)

    def withdraw(self, amount, description=''):
        neg_amount = 0 - amount
        fund_checker = self.check_funds(amount)
        if fund_checker is True:
            _withdraw = {'amount': neg_amount, 'description': description}
            self.ledger.append(_withdraw)
            return True
        else:
            return False

    def transfer(self, amount, budget_category):
        fund_checker = self.check_funds(amount)
        if fund_checker is True:
            self.withdraw(amount, 'Transfer to {}'.format(budget_category.name))
            budget_category.deposit(amount, 'Transfer from {}'.format(self.name))
            return True
        else:
            return False
