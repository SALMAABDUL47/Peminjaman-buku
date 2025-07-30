from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peminjaman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Peminjaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_peminjam = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), nullable=False)
    judul_buku = db.Column(db.String(200), nullable=False)
    tanggal_pinjam = db.Column(db.String(20), nullable=False)
    tanggal_kembali = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nama_peminjam": self.nama_peminjam,
            "nim": self.nim,
            "judul_buku": self.judul_buku,
            "tanggal_pinjam": self.tanggal_pinjam,
            "tanggal_kembali": self.tanggal_kembali
        }

with app.app_context():
    db.create_all()

@app.route('/peminjaman', methods=['GET'])
def get_all():
    data = Peminjaman.query.all()
    return jsonify([d.to_dict() for d in data])

@app.route('/peminjaman', methods=['POST'])
def create():
    data = request.json
    new_data = Peminjaman(**data)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data peminjaman berhasil ditambahkan."}), 201

@app.route('/peminjaman/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    pinjam = Peminjaman.query.get(id)
    if not pinjam:
        return jsonify({"error": "Data tidak ditemukan"}), 404

    pinjam.nama_peminjam = data['nama_peminjam']
    pinjam.nim = data['nim']
    pinjam.judul_buku = data['judul_buku']
    pinjam.tanggal_pinjam = data['tanggal_pinjam']
    pinjam.tanggal_kembali = data['tanggal_kembali']
    db.session.commit()
    return jsonify({"message": "Data berhasil diupdate"})

@app.route('/peminjaman/<int:id>', methods=['DELETE'])
def delete(id):
    pinjam = Peminjaman.query.get(id)
    if not pinjam:
        return jsonify({"error": "Data tidak ditemukan"}), 404

    db.session.delete(pinjam)
    db.session.commit()
    return jsonify({"message": "Data berhasil dihapus"})

if __name__ == '__main__':
    app.run(debug=True)
