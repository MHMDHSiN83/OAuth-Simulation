from flask import Flask, render_template, request, jsonify, redirect, render_template_string
from auth_server import AuthServer
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.pardir, 'templates'), 
            static_folder=os.path.join(os.pardir, 'static'))
auth_server = AuthServer()

@app.route('/login', methods=['GET'])
def show_login_form():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope', 'email')
    return render_template('login_page.html', client_id=client_id, redirect_uri=redirect_uri, scope=scope)

@app.route('/login', methods=['POST']) 
def login():
    client_id = request.form.get('client_id')
    redirect_uri = request.form.get('redirect_uri')
    phone = request.form.get('phone')
    password = request.form.get('password')
    scope = request.form.get('scope', 'email')

    # Authenticate user
    user = AuthServer.authenticate_user(phone, password)
    if user:
        return render_template('confirmation_page.html', client_id=client_id, redirect_uri=redirect_uri, username=phone, scope=scope, email=user.get_email(), phone=user.get_phone(), name=user.get_name())
    else:
        return "Invalid credentials", 401

@app.route('/confirm', methods=['POST'])
def confirm():
    client_id = request.form.get('client_id')
    redirect_uri = request.form.get('redirect_uri')
    username = request.form.get('username')
    scope = request.form.get('scope', 'email')

    # Issue authorization code after confirmation
    auth_code = AuthServer.issue_authorization_code(client_id, username)
    return redirect(f"{redirect_uri}?code={auth_code}&scope={scope}")

@app.route('/token', methods=['POST'])
def token():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    code = request.form.get('code')
    scope = request.form.get('scope', 'email')

    if auth_server.validate_client(client_id, client_secret):
        if auth_server.validate_authorization_code(code, client_id):
            access_token = auth_server.generate_access_token(code)
            return jsonify({
                'access_token': access_token,
                'token_type': 'bearer',
                'expires_in': 3600,
                'scope': scope
            })
        else:
            return jsonify({'error': 'Invalid authorization code'}), 401
    else:
        return jsonify({'error': 'Invalid client credentials'}), 401

@app.route('/user_info', methods=['POST'])
def user_info():
    access_token = request.headers.get('Authorization').replace('Bearer ', '')
    scope = request.form.get('scope')

    if access_token:
        username = auth_server.get_username_from_token(access_token)
        if username:
            user = auth_server.users.get(username)
            if user:
                user_info = auth_server.get_user_data(user, scope)
                return jsonify(user_info)
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Invalid or expired access token'}), 401
    else:
        return jsonify({'error': 'Invalid access token'}), 401

if __name__ == '__main__':
    app.run(port=5000)
