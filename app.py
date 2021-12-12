from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
 


app = Flask(__name__)
app.secret_key = "secret"

cred = credentials.Certificate("rdhkey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# mhs1 = {
#     "nama" : "Ridha",
#     "nilai" : 96,.
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

    nama1= db.collection("Pegawai").document(session["idlogin"]).get().to_dict()["nama"]
    nilai1= db.collection("Pegawai").document(session["idlogin"]).get().to_dict()["nilai"]
    mahasiswa = ["Nunung", "Ridha", "Ridha2", "Nunung2"]

    return render_template('index.html', mahasiswa=mahasiswa, nama1=nama1, nilai1=nilai1)

    # nama = "Ridha"
    # nilai = 82
    # if nilai > 90:
    #     lulus = 1
    # elif nilai > 80:
    #     lulus = 2
    # else:
    #     lulus = 3

    # return render_template('index.html', nama=nama, nilai=nilai, lulus=lulus)
@app.route('/hapus/<sbr>')
def hapus(sbr):
    db.collection("Pegawai").document(sbr).delete()
    return redirect(url_for("index"))

@app.route('/profil')
def profil():
    if "login" not in session:
        return redirect(url_for("login"))
    
    list_mahasiswa = []    
    docs = db.collection("Pegawai").order_by("nilai", direction=firestore.Query.DESCENDING).limit(5).stream()
    for doc in docs:
        pgw = doc.to_dict()
        pgw["sbr"] = doc.id
        # append memasukkan data base ke itu list mahasiswa
        list_mahasiswa.append(pgw)

    nama1= db.collection("Pegawai").document(session["idlogin"]).get().to_dict()["nama"]

    return render_template('profil.html', data1=list_mahasiswa, nama1=nama1)
    

@app.route('/login', methods=["GET", "POST"])
def login():
    if "login" in session:
        return redirect(url_for("index"))
    
    pesan = ""
    if request.method == "GET":
        return render_template('login.html', pesan=pesan, warna="danger", logo1="#exclamation-triangle-fill")

        
    docs = db.collection("Pegawai").where("nama", "==", request.form["username"]).stream()
    pesan = "username salah" 
    for doc in docs:
        pgw = doc.to_dict()
        if request.form["password"] == pgw["password"]:
            session["login"] = True
            # session["pengguna"] = pgw["nama"]
            session["idlogin"] = doc.id
            return redirect(url_for("index"))
        else:
            pesan = "password salah"
            

    return render_template('login.html', pesan=pesan, warna="danger", logo1="#exclamation-triangle-fill" )

@app.route('/dashboard', methods=["GET", "POST"])
def Dashboard():
    if "login" not in session:
        return redirect(url_for("login"))

    pesan = ""

    if request.method == "POST":
        doc_ref = db.collection("Pegawai").document(session["idlogin"])
        data2 = {
            "nama": request.form["username"],
            "nilai": int(request.form["nilai"]),
            "password": request.form["password"],
        }
        doc_ref.update(data2)
        pesan = "Data Berhasil di ubah"
        return render_template("dashboard.html", nama1=data2["nama"], nilai1=data2["nilai"], pesan=pesan )

    
    list_mahasiswa = []    
    docs = db.collection("Pegawai").stream()
    for doc in docs:
        pgw = doc.to_dict()
        # append memasukkan data base ke itu list mahasiswa
        list_mahasiswa.append(pgw)

    nama1= db.collection("Pegawai").document(session["idlogin"]).get().to_dict()["nama"]
    nilai1= db.collection("Pegawai").document(session["idlogin"]).get().to_dict()["nilai"]
    return render_template('dashboard.html', nama1=nama1, nilai1=nilai1, pesan=pesan)
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if "login" in session:
        return redirect(url_for("index"))

    pesan = ""

    if request.method == "POST":
        docs = db.collection("Pegawai").where("nama", "==", request.form["username"]).stream()
        for doc in docs:
            pesan = "User telah terdaftar"
            return render_template("register.html", pesan=pesan, warna="danger", logo1="#exclamation-triangle-fill")

        data = {
            "nama": request.form["username"],
            "nilai": int(request.form["nilai"]),
            "password": request.form["password"]
        }

        db.collection("Pegawai").add(data)
        pesan = "Pendaftaran Berhasil"
        return render_template('login.html', pesan=pesan, warna="primary", logo1="#check-circle-fill")
    return render_template('register.html', pesan=pesan)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/Halo/<nama>')
def Halo(nama):
    return render_template('halo.html', nama=nama)

@app.route('/api/pgw/detail/<id_nama>')
def api_pgw(id_nama):
    pgw = db.collection("Pegawai").document(id_nama).get().to_dict()
    return jsonify(pgw["deskripsi"])

if __name__ == "__main__":
    app.run(debug=True)