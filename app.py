from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_crud'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

def create_table():
    try:
        cur = mysql.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY ,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
            '''
        )
        mysql.commit()
        cur.close()
    except Exception as e:
        print("Error while creating table",e)


@app.route('/')
def hello():
    return 'Your Flask Server Running'

@app.route('/additems', methods=['POST'])
def add_items():
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
        cur = mysql.cursor()
        cur.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (name, description))
        mysql.commit()
        cur.close()
        response = {
            'error' : False,
            'message': 'Item Added Successfully',
            'data': data         
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500

@app.route('/getitems', methods = ['GET'])
def get_items():
    try:
        cur = mysql.cursor()
        cur.execute('SELECT * FROM items')
        data = cur.fetchall()
        cur.close()
        items = [{ 'id': item[0], 'name': item[1], 'description': item[2]} for item in data]
        response = {
            'error' : False,
            'message': 'Items Fetched Successfully',
            'data': items         
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500
    
@app.route('/updateitems/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
        cur = mysql.cursor()
        cur.execute('UPDATE items SET name = %s, description = %s WHERE id = %s', (name, description, item_id))
        mysql.commit()
        cur.close()
        response = {
            'error' : False,
            'message': 'Items Updated Successfully',
            'data': { 'item_id': item_id }
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500
    
@app.route('/deleteitems/<int:item_id>', methods=['DELETE'])
def delete_items(item_id):
    try:
        cur = mysql.cursor()
        cur.execute('DELETE FROM items WHERE id = %s',(item_id))
        mysql.commit()
        cur.close()
        response = {
            'error' : False,
            'message': 'Item Deleted Successfully',
            'data': { 'item_id': item_id }
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500
    
if __name__ == '__main__':
    create_table()
    app.run(debug=True)