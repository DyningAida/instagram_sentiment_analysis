# import library
from flask import Flask, render_template, request
from instascrape import Profile
from textblob import TextBlob
import re, random
from langdetect import detect
from google_trans_new import google_translator  

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # mengambil inputan username dari form
        username = request.form['username']
        # mengambil data profile sesuai username yang diinput
        ig = Profile(username)
        # give session id to scrap
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
            "cookie": "sessionid=2055545287%3AarnEjTWjTxeh7f%3A4;"
        }
        try:
            # scrap data profil
            ig.scrape(headers=headers)
            # mengambil data recent post
            ig_posts = ig.get_recent_posts()
            posts = []
            time = []
            sentim = []
            caption_list = []
            num = []
            polarity = []
            i = 0
            for post in ig_posts:
                # scrap post
                post.scrape(headers=headers)
                # menambahkan data post yang discrap, mengubah ke dict dan append ke posts list
                posts.append(post.to_dict())
                # lower & clean data caption
                caption = ' '.join(re.sub("(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\s+)", " ",str(posts[i]['caption']).lower()).split())
                # memasukkan ke caption list
                caption_list.append(caption)
                # jika terdeteksi caption selain bahasa inggis, maka translate untuk cek polaritynya
                if detect(str(caption)) != 'en':
                    # translate ke bahasa inggris
                    translator = google_translator()
                    eng_capt = translator.translate(caption,lang_tgt='en')
                else:
                    eng_capt = caption
                # blob caption
                eng_capt = TextBlob(eng_capt)
                # cek apakah caption ada atau tidak, jika ada, maka hitung polarity
                if str(caption) != 'nan':
                    if eng_capt.sentiment.polarity < 0:
                        sentiment = 'negative'
                    elif eng_capt.sentiment.polarity == 0:
                        sentiment = 'neutral'
                    else:
                        sentiment = 'positive'
                else:
                    # jika tidak ada caption
                    sentiment = 'no sentiment'
                # mengambil nilai polarity
                polarity_value = eng_capt.sentiment.polarity
                polarity.append(polarity_value)
                # mengambil waktu upload
                upload_time = posts[i]['upload_date']
                time.append(upload_time)
                # memasukkan sentiment
                sentim.append(sentiment)
                i += 1
            for x in range(len(posts)):
                # untuk mengurutkan data
                num.append(x+1)
            # total data
            amount_data = len(posts)
            # satukan data yang dibutuhkan      
            list_data = list(zip(num, time, caption_list, polarity, sentim))
            return render_template('index.html', list_data=list_data, amount_data=amount_data, username=username)
        except:
            return render_template('none.html')
    return render_template('layout.html')
#if __name__ == "__main__":
#    app.run(debug=True)