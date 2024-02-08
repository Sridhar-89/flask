from flask import Flask, jsonify, request
import csv

app = Flask(__name__)
file = 'accounts.csv'

# Code to read accounts from accounts.csv
def reading_accounts():
    accounts = []
    with open(file, 'r') as f:
        rows = csv.DictReader(f)
        for row in rows:
            accounts.append(row)
    return accounts

# Code to write accounts into accounts.csv file
def writing_accounts(accounts):
    with open(file, 'w', newline='') as f:
        fields = ['id', 'name', 'balance']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for account in accounts:
            writer.writerow(account)

# code to get all the accounts
@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = reading_accounts()
    if len(accounts)==0 :
        return jsonify({'message': 'No account found'}), 404
    return jsonify({'accounts': accounts}), 200

# Code to get a specific account by account id
@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    accounts = reading_accounts()
    for acc in accounts:
        if(int(acc['id'])==account_id):
            return jsonify(acc)
    return jsonify({'message': 'Account not found'}), 404

# Code to create a new account
@app.route('/accounts', methods=['POST'])
def create_account():
    accounts = reading_accounts()
    new_account = {
        'id': len(accounts) + 1,
        'name': request.json['name'],
        'balance': request.json['balance']
    }
    accounts.append(new_account)
    writing_accounts(accounts)
    return jsonify({'message': 'Account created', 'account': new_account}), 201

# Code to update an existing account
@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    accounts = reading_accounts()
    for acc in accounts:
        if int(acc['id'])==account_id:
            acc['name'] = request.json['name']
            acc['balance'] = request.json['balance']
            writing_accounts(accounts)
            return jsonify({'message': 'Account updated', 'account': acc}), 200
    return jsonify({'message': 'Account not found'}), 404

# Code to delete a account by account id
@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    accounts = reading_accounts()
    for acc in accounts:
        if(int(acc['id'])==account_id):
            accounts.remove(acc)
            writing_accounts(accounts)
            return jsonify({'message': 'Account deleted'}), 200
    return jsonify({'message': 'Account not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
