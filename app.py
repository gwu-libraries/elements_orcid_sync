from flask import Flask, request, jsonify
import requests
import psycopg2
import os

app = Flask(__name__)

# TODO: Read this in from the DB extract
# TODO: Really, query the DB when a request comes in
app.tokens = {os.getenv('ORCID'): os.getenv('ORCID_TOKEN')}

orcid_endpoints = {'membership': '/membership',
                   }

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'mydatabase'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'db'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    return conn

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/add-service', methods=['POST'])
def add_service():
    '''
    Add a distinction item for a specific orcid_id
    Data should be of the form:
    {orcid_id: '0000-0000-0000-0000',
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
    orcid_token = app.tokens[orcid_id]
    # If we don't have the token, or orcid_id wasn't specified, return an error
    if not orcid_id or not item_data:
        return jsonify({"error": "Missing ORCID ID or membership data"}), 400

    # If we have the token, use it to add the membership to the profile
#    headers = os.getenv('ORCID_HEADERS')
#    headers['Authorization'] += orcid_token
    headers = {
        "Authorization": f"Bearer {orcid_token}",
        "Content-Type": "application/vnd.orcid+json"
    }
    # Get the appropriate ORCiD API endpoint
    orcid_endpoint_url = f"{os.getenv('ORCID_URL')}/{orcid_id}/{item_type}"
    response = requests.post(orcid_endpoint_url, headers=headers, json=item_data)

    if response.status_code == 201:
        return jsonify({"message": f'{item_type} item added successfully'}), 201
    else:
        return jsonify({"error": response.json()}), response.status_code

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

