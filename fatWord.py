import pykakasi
import re
import pandas as pd


def message_generate(query):
    # ユーザー側の入力ワード
    target_word_origin = query

# 3段階でワードリストを作る
# 「太る」ベクトルはなくす？
# 4文字で分ける
# 1~4
# 4~7
# 6~10

    # ローマ字へ変換
    kakasi = pykakasi.kakasi()

    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')

    conv = kakasi.getConverter()
    target_word = conv.do(target_word_origin)

    # 母音のみ残す
    target_word_vo = re.sub(r"[^aeiou]+", "", target_word)

    # このdfの右辺に挿入するものを入れていく感じ
    # 短め単語リスト
#    df = pd.read_csv('/home/denham/OpenHackU_vol_4_ID3/ver2.csv')
    # 長め単語リスト
    df = pd.read_csv('/home/denham/OpenHackU_vol_4_ID3/ver3.csv')

    df['ローマ字'] = df['原文'].apply(convert_to_romaji)
    df['抽出'] = df['ローマ字'].apply(get_vowel)

    # ここではpandas.core.series.Series型になっている
    # print(type(df['抽出']))

    # とりあえず配列にぶち込む
    df['抽出'].values

    # 要素がlist型として認識された！
    # type(df['抽出'].values[0])
    # print(df['抽出'].values[0])

    i = 0
    vowel_list = ' '
    # 母音のリストを文字列に叩き込むためにfor文で順番に後ろから追加していく
    for list in df['抽出'].values:
        Str = "".join(df['抽出'].values[i])
        vowel_list += Str+' '
        i += 1

    data_list = df['原文'].values
    data_list_vo = df['ローマ字'].values

    # vowel_dataのインデックスで母音変換前のdataが分かるように辞書作成。
    dic = {k: v for k, v in enumerate(data_list)}

    ranking = get_idx_score(data_list_vo, target_word_vo)
    # print(data_list_vo)
    # print(target_word_vo)
    for i in range(len(ranking)):
        idx = ranking[i][0]
        score = ranking[i][1]
        # print("スコア:" + str(score))
        # print("言葉:" + dic[idx])
        index = ranking[0][0]
        max = dic[index]
        result = max
    return result

# 短い方のwordをスライスし、他方にそれが含まれていた場合「韻」と見なし、その長さをスコアとして加算する


def make_score(word_a, word_b):
    score = 0
    count = 0

    # 読み込む文字列がリストよりも長い場合
    if len(word_a) > len(word_b):

      # 文字列が短すぎる場合、マイナス報酬を与える
        score += (len(word_b) - len(word_a))*1.1

        word_len = len(word_b)
        for i in range(word_len):
            for j in range(word_len + 1):
                if word_b[i:j] in word_a:

                    # 末尾の得点変化率を強くする
                    if count == word_len-1:
                        score += len(word_b[i:j])*2.6
                    # 後ろから2文字目の得点変化率を強くする
                    elif count == word_len - 2:
                        score += len(word_b[i:j])*2.5
                        count += 1
                    # 文頭の得点変化率を強くする
                    elif count == 0:
                        score += len(word_b[i:j])*1.5
                        count += 1
                    # 文頭・末尾以外の処理
                    else:
                        score += len(word_b[i:j])
                        count += 1

       # 読み込む文字列がリストよりも短い場合
    else:
       # 文字列が長すぎる場合、マイナス報酬を与える
        score += (len(word_a) - len(word_b))*1.2

        word_len = len(word_a)
        for i in range(word_len):
            for j in range(word_len + 1):
                if word_a[i:j] in word_b:

                    # 後ろから2文字目の得点変化率を強くする
                    if count == word_len-2:
                        score += len(word_a[i:j])*2.5
                        count += 1
                    # 文末の得点変化率を強くする
                    elif count == word_len-1:
                        score += len(word_a[i:j])*3.6
                    # 文頭の得点変化率を強くする
                    elif count == 0:
                        score += len(word_a[i:j])*1.5
                        count += 1
                    # 文頭・末尾以外の処理
                    else:
                        score += len(word_a[i:j])
                        count += 1
    return score
# それぞれ母音のみにしたデータと任意の言葉を渡す。後に元の言葉が分かるようインデックスとスコアをセットで取得。


def get_idx_score(vowel_data, target_word):
    ranking = []
    for i, word_b in enumerate(vowel_data):
        score = make_score(target_word, word_b)
        ranking.append([i, score])

    return sorted(ranking, key=lambda x: -x[1])


def get_vowel(doc):
    return re.findall('n[qwrtypsdfghjklzxcvbnm]|[aiueo]', doc)


def convert_to_romaji(text):

    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")        # Hiragana to ascii
    kakasi.setMode("K", "a")        # Katakana to ascii
    kakasi.setMode("J", "a")        # Japanese to ascii
    kakasi.setMode("r", "Hepburn")  # use Hepburn Roman table
    kakasi.setMode("s", True)       # add space
    kakasi.setMode("C", False)      # no capitalize
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result
