import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000/peminjaman"

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

st.title("📚 Sistem Peminjaman Buku - Perpustakaan Kampus")

menu = st.sidebar.selectbox("Pilih Menu", ["Lihat Peminjaman", "Tambah Peminjaman", "Ubah Peminjaman", "Hapus Peminjaman"])

if menu == "Lihat Peminjaman":
    st.header("📖 Daftar Peminjaman Buku")
    res = requests.get(BASE_URL)
    data = res.json()
    if data:
        df = pd.DataFrame(data)
        df.set_index("id", inplace=True)
        st.dataframe(df)
    else:
        st.info("Belum ada data peminjaman.")

elif menu == "Tambah Peminjaman":
    st.header("➕ Tambah Data Peminjaman")
    nama = st.text_input("Nama Peminjam")
    nim = st.text_input("NIM")
    judul = st.text_input("Judul Buku")
    tgl_pinjam = st.date_input("Tanggal Pinjam").strftime("%Y-%m-%d")
    tgl_kembali = st.date_input("Tanggal Kembali").strftime("%Y-%m-%d")
    if st.button("Simpan"):
        if nama and nim and judul:
            data = {
                "nama_peminjam": nama,
                "nim": nim,
                "judul_buku": judul,
                "tanggal_pinjam": tgl_pinjam,
                "tanggal_kembali": tgl_kembali
            }
            res = requests.post(BASE_URL, json=data)
            st.success(res.json().get("message", "Berhasil ditambahkan!"))
            st.balloons()
        else:
            st.warning("Semua kolom wajib diisi.")

elif menu == "Ubah Peminjaman":
    st.header("✏️ Ubah Data Peminjaman")
    id_edit = st.number_input("Masukkan ID peminjaman", min_value=1, step=1)
    nama = st.text_input("Nama Peminjam (baru)")
    nim = st.text_input("NIM (baru)")
    judul = st.text_input("Judul Buku (baru)")
    tgl_pinjam = st.date_input("Tanggal Pinjam (baru)").strftime("%Y-%m-%d")
    tgl_kembali = st.date_input("Tanggal Kembali (baru)").strftime("%Y-%m-%d")
    if st.button("Update"):
        data = {
            "nama_peminjam": nama,
            "nim": nim,
            "judul_buku": judul,
            "tanggal_pinjam": tgl_pinjam,
            "tanggal_kembali": tgl_kembali
        }
        res = requests.put(f"{BASE_URL}/{id_edit}", json=data)
        if res.status_code == 200:
            st.success("Data berhasil diupdate.")
        else:
            st.error("Gagal mengupdate data.")

elif menu == "Hapus Peminjaman":
    st.header("🗑️ Hapus Data Peminjaman")
    id_delete = st.number_input("Masukkan ID peminjaman yang ingin dihapus", min_value=1, step=1)
    if st.button("Hapus"):
        res = requests.delete(f"{BASE_URL}/{id_delete}")
        if res.status_code == 200:
            st.success("Data berhasil dihapus.")
        else:
            st.error("Gagal menghapus data.")
