# UTS AI Instagram Sentiment Analysis 
# (Dyning Aida Batrishya 1184030)
---
Aplikasi ini menggunakan library insta-scrape untuk melakukan scrap data dari instagram, google_trans_new untuk translate caption, textblob untuk menghitung nilai polarity.

Data yang diambil dari instagram ialah 
- upload date untuk waktu post, dan 
- data caption berdasarkan recent post akun untuk analisis sentiment, maksimal sebanyak 12 data. 

Nilai sentiment dihasilkan dari hasil polarity dari setiap caption, yakni apabila :
- nilai sentiment polarity < 0, maka bernilai negative
- nilai sentiment polarity = 0, maka bernilai neutral
- nilai sentiment polarity > 0, maka bernilai positive

Kemudian, karena tidak semua post instagram memiliki caption. Maka, bagi yang tidak ada caption di recent postnya, akan menghasilkan 'no sentiment' pada kolom sentiment

Cara kerja :
1. Inputkan username sesuai yang terdaftar di instagram
2. Jika username tidak terdaftar di instagram, maka akan melakukan exception dan render ke halaman none.html
