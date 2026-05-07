# Dashboard Analisis Pasar Kerja

Dashboard ini menampilkan analisis pasar kerja berbasis data lowongan, dengan fokus pada tiga area utama:

- Ringkasan lowongan dan industri
- Skill yang paling sering dicari
- Distribusi gaji per industri dan skill bernilai tinggi

Aplikasi dibangun dengan **Streamlit** dan visualisasi menggunakan **Matplotlib** serta **Seaborn**.

## Cara Menjalankan

1. Pastikan Python sudah terpasang.
2. Install dependensi:

```bash
pip install -r requirements.txt
```

3. Jalankan dashboard:

```bash
streamlit run dashboard/dashboard.py
```

## Struktur Proyek

```text
Capstone Project/
├── dashboard/
│   ├── dashboard.py
│   └── all_jobs_data.csv
├── data/
│   ├── job_market.csv
│   └── job_recommendation_dataset.csv
├── notebook.ipynb
├── requirements.txt
└── url.txt
```

## Dataset Utama: `all_jobs_data.csv`

Dataset utama yang dipakai dashboard berada di folder `dashboard/` dengan nama `all_jobs_data.csv`. Dataset ini berisi **50.200 baris** data lowongan kerja yang sudah dirapikan untuk analisis dashboard.

Dataset ini digunakan untuk menghitung:

- total lowongan
- jumlah perusahaan
- jumlah industri/kategori
- rata-rata gaji
- skill yang paling sering muncul
- skill dengan gaji rata-rata tertinggi

### Penjelasan Kolom

| Kolom | Penjelasan |
|---|---|
| `job_title` | Nama posisi atau jabatan lowongan |
| `company` | Nama perusahaan yang membuka lowongan |
| `category` | Kategori industri/area pekerjaan |
| `skills` | Skill yang dibutuhkan dalam bentuk teks |
| `skills_list` | Daftar skill yang sudah diparse menjadi list untuk analisis |
| `salary` | Nilai gaji numerik dalam USD |
| `experience_level` | Level pengalaman yang dibutuhkan |

### Catatan Dataset

- Kolom `skills_list` dipakai agar skill bisa dihitung per item, bukan hanya sebagai teks mentah.
- Kolom `salary` sudah dikonversi menjadi numerik supaya bisa dihitung rata-ratanya.
- Beberapa nilai bisa berisi informasi seperti `Not Specified` pada level pengalaman jika data asli tidak menyediakan detail lengkap.

## Dataset Pendukung

Folder `data/` berisi dataset tambahan yang bisa dipakai untuk eksplorasi atau pengembangan lanjutan:

- `job_market.csv`
- `job_recommendation_dataset.csv`

Keduanya tidak digunakan langsung oleh dashboard utama saat ini, tetapi berguna untuk analisis tambahan atau pengembangan fitur berikutnya.

## Teknologi yang Dipakai

- `streamlit`
- `pandas`
- `matplotlib`
- `seaborn`
- `Babel`

## Hasil yang Ditampilkan Dashboard

- Grafik skill paling dicari
- Grafik industri dengan volume lowongan terbesar
- Grafik distribusi gaji per industri
- Top 10 skill dengan gaji tertinggi
- Insight dan kesimpulan otomatis dari data
