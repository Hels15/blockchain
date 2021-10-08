from hashlib import sha256
from datetime import datetime


class Block:
    def __init__(self, data, time=datetime.today(), pre_hash='0' * 64):
        self.time = time
        self.data = data
        self.pre_hash = pre_hash
        self.nonce = 0
        self.hash = self.make_hash()

    def __str__(self):
        text = ''
        for row in self.__dict__.items():
            if type(row[1]) == list:
                for transaction in row[1]:
                    text += transaction.sender + '-' + transaction.receiver + '-' + str(transaction.amount) + ' '
                    text += '\n'
            else:
                text += str(row[0]) + ":" + str(row[1]) + '\n'

        return text

    def make_hash(self):
        return sha256((str(self.time) + ''.join(str(transaction) for transaction in self.data) + str(
            self.pre_hash) + str(self.nonce)).encode()).hexdigest()

    def mine(self, difficulty):
        print("Start mining:")
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.make_hash()
        print('Experiment:', self.nonce)
        print('Mined:', self.hash, '\n')




class Blockchain:
    def __init__(self):
        self.chain = [self.genesis_block()]
        self.difficulty = 4
        self.reward = 25
        self.transaction_list = []

    def __str__(self):
        text = ''
        for block in self.chain:
            text += '\n' + str(block)
            text += '\n----------------------------'
        return text

    def genesis_block(self):
        return Block('Genesis block')

    def new_transaction(self, transaction):
        self.transaction_list.append(transaction)

    def mine_transactions(self, miner):
        block = Block(self.transaction_list, pre_hash=self.chain[-1].hash)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.transaction_list = [Transaction('hels', miner, self.reward)]

    def is_valid(self):
        for i in range(len(self.chain) - 1):
            if self.chain[i].hash != self.chain[i + 1].pre_hash:
                return 'Previous hash conflict defected in' + str(i + 1) + '. block!'
            if self.chain[i].hash != self.chain[i].make_hash():
                return 'Own hash conflict defected in ' + str(i + 1) + '. block!'
        return 'OK'

    def get_balance(self, person):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver == person:
                    balance += transaction.amount

                if transaction.sender == person:
                    balance -= transaction.amount

        return balance


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        text = ''
        for row in self.__dict__.items():
            text += str(row[0]) + ":" + str(row[1]) + '\n'
        return text


pk_coin = Blockchain()

print('\n>>>GENESIS BLOCK >>>')
print(pk_coin)

pk_coin.new_transaction(Transaction("Luke", "Han", 5))
pk_coin.new_transaction(Transaction("Obi-wan", "Han", 150))
pk_coin.new_transaction(Transaction("Han", "Yoda", 200))

# print('>>>TRANSACTION>>>')
# for item in pk_coin.transaction_list:
#     print(item)
pk_coin.mine_transactions('Yoda')

print('>>>BLOCKS>>>')
print(pk_coin)
#
# print('>>>TRANSACTION>>>')
# for item in pk_coin.transaction_list:
#     print(item)


#print(">>> BALANCE >>>")


print('>>>MINING>>>')
pk_coin.mine_transactions('Yoda')

print('Luke', pk_coin.get_balance('Luke'))
# print('>>>BLOCKS>>>')
# print(pk_coin)

print("Is valid", pk_coin.is_valid())

pk_coin.chain[1].data[0].amount = 100
print('Is valid?', pk_coin.is_valid())

pk_coin.chain[1].hash = pk_coin.chain[1].make_hash()
print('Is valid?', pk_coin.is_valid())

