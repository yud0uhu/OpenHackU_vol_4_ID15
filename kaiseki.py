from bs4 import BeautifulSoup
import MeCab
from gensim.models import word2vec


def word_kaiseki(query):
    path_to_html = 'aozorabunko/cards/000879/files/127_15260.html'

    with open(path_to_html, 'rb') as html:
        soup = BeautifulSoup(html, 'lxml')

    main_text = soup.find("div", class_='main_text')

    # ルビが振ってあるのを削除
    for yomigana in main_text.find_all(["rp", "h4", "rt"]):
        yomigana.decompose()

    sentences = [line.strip() for line in main_text.text.strip().splitlines()]

    print(sentences)

    rashomon_text = ','.join(sentences)

    mecab_wakachi = MeCab.Tagger("-Owakati")
    rashomon_text_wakachi = mecab_wakachi.parse(rashomon_text)
    print(rashomon_text_wakachi)

    model = word2vec.Word2Vec(rashomon_text_wakachi, size=100,
                              min_count=5, window=5, iter=3)  # windowは小さすぎると関連づけがされにくくなる
    model.save("word2vec.gensim.model")  # ここでモデルセットをセーブ
    # model = gensim.models.Word2Vec.load('word2vec.gensim.model') # saveはロードでよみこむ

    model = word2vec.Word2Vec.load('word2vec.gensim.model')
    results = model.wv.most_similar(query)  # ここで母音セットを渡したい
    for result in results:
        print(result)
    return result
