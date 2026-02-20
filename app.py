from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (In a real application, this would be replaced with a database)
reminders = []

@app.route('/reminders', methods=['GET'])
def get_reminders():
    return jsonify(reminders), 200

@app.route('/reminders', methods=['POST'])
def create_reminder():
    data = request.get_json()
    reminder = {'id': len(reminders) + 1, 'task': data['task']}
    reminders.append(reminder)
    return jsonify(reminder), 201

@app.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    global reminders
    reminders = [r for r in reminders if r['id'] != reminder_id]
    return jsonify({'result': True}), 204

if __name__ == '__main__':
    app.run(debug=True)