from flask import Flask, request, jsonify
import requests
import psycopg2
import os

app = Flask(__name__)

# TODO: Read this in from the DB extract
# TODO: Really, query the DB when a request comes in
# app.tokens = {os.getenv('ORCID'): os.getenv('ORCID_TOKEN')}

# orcid_endpoints = {'membership': '/membership', }

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'mydatabase'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'db'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    return conn

@app.route('/db-test', methods=['GET'])
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'db_version': db_version[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_orcid_token(orcid_id):
    '''
    Return the token for a given ORCiD ID
    TODO: Retrieve this from the DB instead
    '''
    return ''
    # return app.tokens[orcid_id]
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute("SELECT token FROM orcid_tokens WHERE orcid_id = %s", (orcid_id,))
    # result = cur.fetchone()
    # cur.close()
    # conn.close()
    # return result[0] if result else None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/add-activity', methods=['POST'])
def add_activity():
    '''
    Add a distinction item for a specific orcid_id
    Data should be of the form:
    {orcid_id: '0000-0000-0000-0000',
     orcid_token: 'token-goes-here',
     item_type: 'membership', # or distinction, service, etc.
     item_data: # should be ORCiD-formatted 
      {# see https://github.com/ORCID/orcid-model/blob/master/src/main/resources/record_3.0/samples/write_samples/*.json}
    '''
    data = request.json
    # Extract orcid_id from request
    orcid_id = data.get('orcid_id') # orcid_id of the profile to update
    item_type = data.get('item_type')
    item_data = data.get('item_data') # item info to add to the profile

    # Retrieve token for this orcid_id from the database
    #orcid_token = get_orcid_token(orcid_id)
    orcid_token = data.get('orcid_token')
    if not orcid_id or not orcid_token or not item_data:
        return jsonify({"error": "Missing ORCID ID or ORCID token or membership data"}), 400

    headers = {
        "Authorization": f"Bearer {orcid_token}",
        "Content-Type": "application/vnd.orcid+json"
    }
    orcid_endpoint_url = f"{os.getenv('ORCID_URL')}/{orcid_id}/{item_type}"
    response = requests.post(orcid_endpoint_url, headers=headers, json=item_data)

    if response.status_code == 201:
        return jsonify({"message": f'{item_type} item added successfully'}), 201
    else:
        return jsonify({"error": response.json()}), response.status_code


@app.route('/delete-activity', methods=['POST'])
def delete_activity():
    '''
    Add a distinction item for a specific orcid_id
    Data should be of the form:
    {orcid_id: '0000-0000-0000-0000',
     item_type: 'membership', # or distinction, service, etc.
     item_data: # should be ORCiD-formatted 
      {# see https://github.com/ORCID/orcid-model/blob/master/src/main/resources/record_3.0/samples/write_samples/*.json}
    '''
    data = request.json
    orcid_id = data.get('orcid_id') # orcid_id of the profile to update
    item_type = data.get('item_type')
    orcid_token = data.get('orcid_token')
    activity_id = data.get('activity_id') # This should be the ORCiD put-code of the activity

    if not orcid_id or not orcid_token:
        return jsonify({"error": "Missing ORCID ID or ORCID token or membership data"}), 400

    headers = {
        "Authorization": f"Bearer {orcid_token}",
        "Content-Type": "application/vnd.orcid+json"
    }
    orcid_endpoint_url = f"{os.getenv('ORCID_URL')}/{orcid_id}/{item_type}/{activity_id}"
    response = requests.delete(orcid_endpoint_url, headers=headers)

    if response.status_code == 204:  # 204 is for successful deletion
        return jsonify({"message": f'{item_type} {activity_id} item deleted successfully'}), 201
    else:
        return jsonify({"URL": orcid_endpoint_url, "error": response.json()}), response.status_code
    

@app.route('/get-activities', methods=['GET'])
def get_activities():
    """Retrieve activities for a specific ORCID ID."""
    data = request.json
    orcid_id = data.get('orcid_id') # orcid_id of the profile to update
    
    if not orcid_id:
        return jsonify({"error": "Missing ORCID ID"}), 400
    
    orcid_token = data.get('orcid_token')
    if not orcid_token:
        return jsonify({"error": "Invalid ORCID ID or missing token"}), 400
    
    headers = {
        "Authorization": f"Bearer {orcid_token}",
        "Accept": "application/vnd.orcid+json"
    }
    
    orcid_endpoint_url = f"{os.getenv('ORCID_URL')}/{orcid_id}/activities"  
    
    try:
        response = requests.get(orcid_endpoint_url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)