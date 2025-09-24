Tugas 2:
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


Tugas 3:
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

Tugas 4:
1. AuthenticationForm 
    Django AuthenticationForm adalah form dari Django untuk autentikasi username dan password untuk login. Kelebihannya adalah ketersediannya, kekurangannya tidak ada sistem-sistem seperti Captcha dan 2FA
2. Autentikasi dan Otorisasi
    Autentikasi memverfikasi identitas, cth: django.contrib.auth, authenticate(), login()
    Otorisasi adalah mengecek izin/otoritas yang dimiliki identitas tersebut, cth: is_superuser
3. Session dan Cookies
    Session sederhana dan dapat diakses dari JS. Kekurangannya adalah sizenya yang kecil.
    Cookies disimpan di server side dan lebih besar sizenya. Kekurangannya adalah dalam storage.
4. Keamanan Cookies
    Tidak sepenuhnya aman dengan adanya risiko hal-hal seperti CSRF. Sarannya adalah dengan memvalidasi input dan tidak menyimpan informasi/data penting atau sesnitif di dalam Cookies.
5. Implementasi Checklist
    1. Membuat fungsi registrasi dengan HTMLnya.
    2. Membuat fungsi login dengan HTMLnya.
    3. Membuat fungsi logout dengan HTMLnya.
    4. Mengatur URL
    5. Restrict akses ke akun yang sudah registrasi
    6. Mendaftarkan cookies untuk last login 
    7. Memasukan user ke model
    8. Migrate (jangan lupa)
