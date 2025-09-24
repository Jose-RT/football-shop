Tutorial 2:
1. Implementasi Checklist
    1. Step-step awal dengan Git, env, dan instalasi Django
    2. Membuat proyek Django baru
    3. Membuat aplikasi main
    4. Routing di urls proyek
    5. Membuat models
    6. Membuat show_main di views
    7. Routing di urls main.py
    8. Deployment
2. Request Resposne Django:
    urls.py menentukan URL yang memanggil fungsi
    views.py merupakan program/logika utama aplikasi
    models.py representasi/berbagai karakteristik dari db
    html menentukan tampilan di browser
3. Settings
    settings.py berisi konfigurasi/pengaturan (settings) dari proyek, contohnya mengatur server, db, apps, dan lain-lain
4. Migrasi database
    Migrasi di Django terbagi menjadi makemigrations yang membuat file migrasi dari model lalu migrate melakukan migrasi itu sendiri yang mengubah sesuai model.
5. Mengapa Django
    Django memiliki banyak fitur yang siap dipakai (authorization, admin,d ll) yang memudahkan proyek. Selain itu dokumentasi masalah dan pertanyaan-pertanyaan banyak karena banyak dipakai.


Tutorial 3:
1. Data delivery 
    Data delivery penting untuk konsistensi dan data yang lebih stabil dan cepat.
2. XML atau JSON
    JSON lebih banyak dipakai karena native di JavaScript. Antara JSON dan XML tentunya banyak faktor yang menentukan. Namun secara keseluruhan JSON memiliki lebih banyak pro daripada XML yang biasanya dipakai untuk integrasi sistem lama saja/legacy.
3. is_valid()
    is_valid dipakai pada form untuk melakukan validasi dengan membersihkan data. Kita membutuhkan sehingga data-data yang "kotor" misalnya format, nilai yang tidak boleh, dll tidak masuk sistem.
4. CSRF
    CSRF (Cross-Site Request Forgery) terjadi ketika penyerang membuat permintaan dari site lain atas nama pengguna yang sudah terautentikasi di site target. Kalau tidak ada CSRF token, maka hal-hal speerti mengubah password, melakukan transfer, dan menghapus data dapat terjadi.
5. Implementasi Checklist
    1. Membuat form dengan semua field dari models
    2. Membuat halaman detail menampilkan data
    3. Fixing HTML yang jujur berantakan