from flask import Flask, render_template, request, redirect, session, url_for
from client import Client
import os
app = Flask(__name__, 
            template_folder=os.path.join(os.pardir, 'templates'), 
            static_folder=os.path.join(os.pardir, 'static'))

client = Client(client_id="client_id_123", client_secret="secret_abc", redirect_uri="http://localhost:5001/callback")

app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    message = session.get('message')
    session['message'] = 0
    return render_template('shopping_page.html', user=client.get_logged_user(), message=message)

@app.route('/login')
def login():
    auth_url = f"http://localhost:5000/login?client_id={client.get_client_id()}&redirect_uri={client.get_redirect_uri()}&scope=online_shopping"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    scope = request.args.get('scope', 'email')
    token_response = client.get_token(code, scope)
    access_token = token_response.get('access_token')

    if access_token:
        user_info_response = client.get_user_info(access_token, scope)
        email = user_info_response.get('email')
        phone = user_info_response.get('phone')
        name = user_info_response.get('name')
        error = user_info_response.get('error')
        client.login(email)
        client.set_name_and_phone(name, phone)
        session['message'] = 1
        return redirect(url_for('home'))
    else:
        return 'Failed to retrieve access token', 400


@app.route('/logout')
def logout():
    client.logout()
    session['message'] = 2
    return redirect(url_for('home'))

if __name__ == '__main__':
    session['message'] = 0
    app.run(port=5001)




# flask --app client_app.py --debug run -h localhost -p 5001

# 0 : no message
# 1 : success login 
# 2 : success logout
# 3 : something is wrong