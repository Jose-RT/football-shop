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

Tugas 5:
1. Urutan prioritas pengambilan CSS selector 
    1. Selector elemen/type (div, p) dan pseudo-element (::before) — spesifitas: 0,0,0,1
    2. Class, atribut ([type="text"]) dan pseudo-class (:hover) — spesifitas: 0,0,1,0
    3. ID (#main) — spesifitas: 0,1,0,0
    4. Inline style (style="...") — spesifitas: 1,0,0,0
    5. !important — overrides hampir semua; jika dua deklarasi sama-sama !important, maka yang lebih spesifik atau yang muncul belakangan menang.
    6. Jika spesifitas sama → yang muncul belakangan di stylesheet (atau file yang di-load nanti) menang.
2. Responsive design konsep yang penting
    Pengguna mengakses site dari layar yang berbeda (HP, tablet, laptop). Reponsive design membuat UI tetap teratur. 
3. Margin, border, dan padding
    1. Margin: ruang di luar border, memisahkan satu elemen sama yg lain
    2. Border: garis di sekitar box antara margin dan padding
    3. Padding: space di dalam border
    Contoh:
    .card {
        margin: 16px;
        border: 1px solid #ccc;
        padding: 12px;
    }
4. Flex box dan grid layout
    1. Flex box (CSS Flexible Box): baris atau kolom, alignment, responsive kecil (navbar, centering)
    2. Grid (CSS Grid Layout): baris *dan* kolom, grid kompleks, magazine layout, dashboard
5. Implementasi Checklist
    Tulis HTML (nav, register, login)

Tugas 6:
1. Synchronous request dan asynchronous request
    1. Synchronous request: browser menunggu response sebelum melanjutkan (cth: submit form tradisional maka halaman reload)
    2. Asynchronous request: request dikirim di background (cthnya AJAX), bisa update sebagian halaman tanpa reload
2. Cara kerja AJAX di Django
    1. Client: JavaScript mengirim permintaan ke endpoint Django (POST atau GET)
    2. Include CSRF token (untuk POST/PUT/DELETE)
    3. Server (Django view): menerima request, memproses (validasi, auth), lalu mengembalikan JsonResponse atau status error
    4. Client: menerima JSON, parsing, kemudian memanipulasi DOM sesuai hasil (menampilkan pesan, update list, redirect, dll)
    5. Tidak ada reload halaman penuh kecuali redirect client-side
3. Keuntungan menggunakan AJAX
    1. UI lebih halus dengan transisi/animation saat update
    2. Pengalaman interaktif dengan form submit tanpa reload, live search, dan infinite scroll (misalnya utk sosial media)
    3. Hemat server resources: tidak mengirim ulang seluruh HTML dan lebih cepat
4. Keamanan AJAX untuk Login/Register
    1. Gunakan HTTPS
    2. CSRF protection
    3. Validasi server side (jangan client side)
    4. Gunakan Django auth dan session
    5. Input dan output sanitization (bersihkan dulu)
5. AJAX mempengaruhi UX
    1. Fitur real time (validasi, auto-save) meningkatkan kenyamanan utk user
    2. lebih cepat dan responsif (tanpa full reload)
    3. Pengalaman interaktif seperti infinite scroll untuk sosial media