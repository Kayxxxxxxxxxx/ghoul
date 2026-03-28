from flask import Flask, request, jsonify
import json
import os
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

ADMIN_TOKEN = "SPAMRED2024"
DB_FILE = "/tmp/database.json"

def get_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {'licenses': [], 'logs': []}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_key():
    return 'SPAM-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

@app.route('/api', methods=['GET', 'POST'])
def api():
    action = request.args.get('action') or request.form.get('action')
    
    # VALIDAR LICENÇA (BOT)
    if action == 'validate':
        key = request.form.get('key') or request.args.get('key')
        hwid = request.form.get('hwid') or request.args.get('hwid')
        
        db = get_db()
        found = None
        for lic in db['licenses']:
            if lic['key'] == key:
                found = lic
                break
        
        if not found:
            return jsonify({'valid': False, 'error': 'Chave inválida'})
        
        if found['status'] != 'active':
            return jsonify({'valid': False, 'error': 'Licença inativa'})
        
        if datetime.strptime(found['expires'], '%Y-%m-%d') < datetime.now():
            return jsonify({'valid': False, 'error': 'Licença expirada'})
        
        if found['hwid'] and found['hwid'] != hwid:
            return jsonify({'valid': False, 'error': 'Licença já ativada em outro PC'})
        
        if not found['hwid']:
            found['hwid'] = hwid
            found['activated_at'] = datetime.now().isoformat()
            save_db(db)
        
        return jsonify({
            'valid': True,
            'expires': int(datetime.strptime(found['expires'], '%Y-%m-%d').timestamp()),
            'max_servers': found.get('max_servers', 50),
            'permissions': found.get('permissions', 'all')
        })
    
    # CRIAR LICENÇA (ADMIN)
    if action == 'create':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Token inválido'})
        
        client = request.form.get('client') or request.args.get('client')
        days = int(request.form.get('days', 30))
        max_servers = int(request.form.get('max_servers', 50))
        permissions = request.form.get('permissions', 'all')
        
        if not client:
            return jsonify({'error': 'Nome do cliente obrigatório'})
        
        db = get_db()
        key = generate_key()
        expires = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        new_license = {
            'key': key,
            'client': client,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'expires': expires,
            'max_servers': max_servers,
            'permissions': permissions,
            'hwid': None,
            'activated_at': None
        }
        
        db['licenses'].append(new_license)
        db['logs'].append({
            'action': 'create',
            'key': key,
            'client': client,
            'date': datetime.now().isoformat()
        })
        save_db(db)
        
        return jsonify({'success': True, 'key': key, 'expires': expires, 'client': client})
    
    # LISTAR LICENÇAS (ADMIN)
    if action == 'list':
        token = request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        db = get_db()
        return jsonify(db['licenses'])
    
    # REVOGAR LICENÇA (ADMIN)
    if action == 'revoke':
        token = request.form.get('token') or request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        key = request.form.get('key') or request.args.get('key')
        db = get_db()
        
        for lic in db['licenses']:
            if lic['key'] == key:
                lic['status'] = 'revoked'
                db['logs'].append({
                    'action': 'revoke',
                    'key': key,
                    'date': datetime.now().isoformat()
                })
                save_db(db)
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Chave não encontrada'})
    
    # ESTATÍSTICAS (ADMIN)
    if action == 'stats':
        token = request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        db = get_db()
        active = sum(1 for l in db['licenses'] if l['status'] == 'active')
        activated = sum(1 for l in db['licenses'] if l['hwid'])
        
        return jsonify({
            'total': len(db['licenses']),
            'active': active,
            'activated': activated
        })
    
    # LOGS (ADMIN)
    if action == 'logs':
        token = request.args.get('token')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Não autorizado'})
        
        db = get_db()
        return jsonify(list(reversed(db['logs'])))
    
    return jsonify({'error': 'Ação inválida'})