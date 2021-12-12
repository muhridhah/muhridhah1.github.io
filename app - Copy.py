from flask import Flask, render_template, request, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore



app = Flask(__name__)
app.secret_key = "secret"

cred = credentials.Certificate("rdhkey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# mhs1 = {
#     "nama" : "Ridha",
#     "nilai" : 96,
#     "password" : "123456"
# }
# mhs2 = {
#     "nama" : "Nunung",
#     "nilai" : 99,
#     "password" : "123456nng"
# }
# mhs3 = {
#     "nama" : "Edirga",
#     "nilai" : 79,
#     "password" : "123456edir"
# }
# mhs4 = {
#     "nama" : "Muhammad",
#     "nilai" : 87,
#     "password" : "123456mhd"
# }
# mhs5 = {
#     "nama" : "Anugerah",
#     "nilai" : 99,
#     "password" : "123456anu"
# }



@app.route('/')
def index():
    if "login" not in session:
        return redirect(url_for("login"))
    list_mahasiswa = []    
    docs = db.collection("Pegawai").stream()
    for doc in docs:
        pgw = doc.to_dict()
        # append memasukkan data base ke itu list mahasiswa
        list_mahasiswa.append(pgw)
    
    mahasiswa = ["Nunung", "Ridha", "Ridha2", "Nunung2"]

    return render_template('index.html', mahasiswa=mahasiswa)

    # nama = "Ridha"
    # nilai = 82
    # if nilai > 90:
    #     lulus = 1
    # elif nilai > 80:
    #     lulus = 2
    # else:
    #     lulus = 3

    # return render_template('index.html', nama=nama, nilai=nilai, lulus=lulus)

@app.route('/profil')
def profil():
    if "login" not in session:
        return redirect(url_for("login"))
    
    list_mahasiswa = []    
    docs = db.collection("Pegawai").stream()
    for doc in docs:
        pgw = doc.to_dict()
        # append memasukkan data base ke itu list mahasiswa
        list_mahasiswa.append(pgw)
    

    return render_template('profil.html', data1=list_mahasiswa)
    

@app.route('/login', methods=["GET", "POST"])
def login():
    if "login" in session:
        return redirect(url_for("index"))
    
    pesan = ""
    if request.method == "GET":
        return render_template('login.html', pesan=pesan)

        
    docs = db.collection("Pegawai").stream()
    for doc in docs:
        pgw = doc.to_dict()
        # append memasukkan data base ke itu list mahasiswa
        if request.form["username"] == pgw["nama"]:
            if request.form["password"] == pgw["password"]:
                session["login"] = True
                session["pengguna"] = pgw["nama"]
                session["nilai"] = pgw["nilai"]
                return redirect(url_for("index"))
            else:
                pesan = "password salah"
            break
        else:
            pesan = "username salah" 

    return render_template('login.html', pesan=pesan )

@app.route('/dashboard')
def Dashboard():
    if "login" not in session:
        return redirect(url_for("login"))

    list_mahasiswa = []    
    docs = db.collection("Pegawai").stream()
    for doc in docs:
        pgw = doc.to_dict()
        # append memasukkan data base ke itu list mahasiswa
        list_mahasiswa.append(pgw)



    return render_template('dashboard.html')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/Halo/<nama>')
def Halo(nama):
    return render_template('halo.html', nama=nama)

if __name__ == "__main__":
    app.run(debug=True)