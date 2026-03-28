from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import hashlib
import os
import time
from datetime import datetime, timedelta
import uuid

app = Flask(__name__, static_folder='.')
CORS(app)

ADMIN_TOKEN = "SPAMRED2024"
DB_FILE = "/tmp/database.json"

def get_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({"licenses": [], "logs": []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_key():
    return f"SPAM-{hashlib.md5(f'{time.time()}{uuid.uuid4()}'.encode()).hexdigest()[:12].upper()}"

@app.route('/')
def home():
    return jsonify({"status": "online", "service": "SpamRed License API"})

@app.route('/admin.html')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/api.php', methods=['GET', 'POST'])
def api():
    action = request.args.get('action') or request.form.get('action')
    
    if action == 'validate':
        key = request.form.get('key') or request.args.get('key')
        hwid = request.form.get('hwid') or request.args.get('hwid')
        
        if not key or not hwid:
            return jsonify({'valid': False, 'error': 'Dados incompletos'})
        
        db = get_db()
        for lic in db['licenses']:
            if lic['key'] == key:
                if lic['status'] != 'active':
                    return jsonify({'valid': False, 'error': 'Licença inativa'})
                if datetime.strptime(lic['expires'], '%Y-%m-%d') < datetime.now():
                    return jsonify({'valid': False, 'error': 'Licença expirada'})
                if lic['hwid'] and lic['hwid'] != hwid:
                    return jsonify({'valid': False, 'error': 'Já ativada em outro PC'})
                if not lic['hwid']:
                    lic['hwid'] = hwid
                    lic['activated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_db(db)
                return jsonify({
                    'valid': True,
                    'expires': int(datetime.strptime(lic['expires'], '%Y-%m-%d').timestamp()),
                    'max_servers': lic['max_servers'],
                    'permissions': lic['permissions']
                })
        return jsonify({'valid': False, 'error': 'Chave inválida'})
    
    elif action == 'create':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        client = request.form.get('client') or request.args.get('client')
        days = int(request.form.get('days') or request.args.get('days') or 30)
        max_servers = int(request.form.get('max_servers') or request.args.get('max_servers') or 50)
        permissions = request.form.get('permissions') or request.args.get('permissions') or 'all'
        
        if not client:
            return jsonify({'error': 'Nome do cliente obrigatório'})
        
        db = get_db()
        key = generate_key()
        
        new_lic = {
            'key': key,
            'client': client,
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'expires': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d'),
            'max_servers': max_servers,
            'permissions': permissions,
            'hwid': None,
            'activated_at': None
        }
        
        db['licenses'].append(new_lic)
        save_db(db)
        
        return jsonify({'success': True, 'key': key, 'expires': new_lic['expires'], 'client': client})
    
    elif action == 'list':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        db = get_db()
        return jsonify(db['licenses'])
    
    elif action == 'revoke':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        key = request.form.get('key') or request.args.get('key')
        db = get_db()
        
        for lic in db['licenses']:
            if lic['key'] == key:
                lic['status'] = 'revoked'
                save_db(db)
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Chave não encontrada'})
    
    elif action == 'stats':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        db = get_db()
        active = sum(1 for l in db['licenses'] if l['status'] == 'active')
        activated = sum(1 for l in db['licenses'] if l['hwid'] is not None)
        
        return jsonify({'total': len(db['licenses']), 'active': active, 'activated': activated})
    
    elif action == 'logs':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        db = get_db()
        return jsonify(db['logs'][-50:])
    
    return jsonify({'error': 'Ação inválida'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
