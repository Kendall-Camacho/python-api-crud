from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)
connect = MySQL(app)


@app.route('/users', methods=['GET'])
def list_users():
    cur = connect.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    rv = cur.fetchall()
    if rv != None:
        user = []
        for row in rv:
            user.append({'id': row[0], 'name': row[1], 'email': row[2]})
        return jsonify({'users': user})
    else:
        return jsonify({'users': 'No users found'})


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        cursor = connect.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        user = cursor.fetchone()
        user = {'id': user[0], 'username': user[1], 'email': user[2]}
        return jsonify({'users': user})
    except Exception as e:
        return (str(e))

# register user


@app.route('/users', methods=['POST'])
def register():
    try:
        print(request.json)
        _json = request.json
        _name = _json['username']
        _email = _json['email']
        _password = _json['password']
        _id = _json['id']
        # validate the received values
        if _name and _email and _password and _id and request.method == 'POST':
            # save edits
            sql = "INSERT INTO users(id,username,email,password) VALUES(%s,%s,%s,%s)"
            data = (_id, _name, _email, _password,)
            cursor = connect.connection.cursor()
            cursor.execute(sql, data)
            connect.connection.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return page_not_found()
        return jsonify({'message': 'User created successfully !'})
    except Exception as ex:
        return jsonify({'message': 'An error occurred'})


# delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor = connect.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'})
        connect.connection.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        return (str(e))

# update user


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        cursor = connect.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        user = cursor.fetchone()
        if user != None:
            _json = request.json
            _name = _json['username']
            _email = _json['email']
            _password = _json['password']
            # validate the received values
            if _name and _email and _password and request.method == 'PUT':
                # save edits
                sql = "UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s"
                data = (_name, _email, _password, id,)
                cursor = connect.connection.cursor()
                cursor.execute(sql, data)
                connect.connection.commit()
                resp = jsonify('User updated successfully!')
                resp.status_code = 200
                return resp
            else:
                return page_not_found()
        else:
            return jsonify({'message': 'User not found'})
    except Exception as e:
        return (str(e))

# 404 message
def page_not_found(e):
    return "Sorry, Nothing at this URL.", 404

# 500 message


def internal_server_error(e):
    return "Sorry, unexpected error: {}".format(e), 500


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.run()
