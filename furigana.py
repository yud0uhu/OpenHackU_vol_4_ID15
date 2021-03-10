import sys
import MeCab
import re


def henkan(text):
    hiragana = [chr(i) for i in range(12353, 12436)]
    katakana = [chr(i) for i in range(12449, 12532)]
    kana = ""
    # 読み仮名のカタかなをひらがなに
    for text in list(text):
        for i in range(83):
            if text == katakana[i]:
                kana += hiragana[i]
    return kana


def tohensu(origin, kana):
    origin = "".join(origin)
    kana = "".join(kana)
    return origin, kana


def kanadelete(origin, kana):
    origin = list(origin)
    kana = list(kana)
    num1 = len(origin)
    num2 = len(kana)
    okurigana = ""

    if origin[num1-1] == kana[num2-1] and origin[num1-2] == kana[num2-2]:
        okurigana = origin[num1-2]+origin[num1-1]
        origin[num1-1] = ""
        origin[num1-2] = ""
        kana[num2-1] = ""
        kana[num2-2] = ""
        origin, kana = tohensu(origin, kana)

    elif origin[num1-1] == kana[num2-1]:

        okurigana = origin[num1-1]

        origin[num1-1] = ""
        kana[num2-1] = ""
        origin = "".join(origin)
        kana = "".join(kana)
    else:
        origin, kana = tohensu(origin, kana)

    return origin, kana, okurigana


def main(text):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')  # 空でパースする必要がある
    node = mecab.parseToNode(text)

    text_new = []
    while node:
        origin = node.surface  # もとの単語を代入
        yomi = node.feature.split(",")[7]  # 読み仮名を代入
        kana = henkan(yomi)

        # 正規表現で漢字と一致するかをチェック
        pattern = "[一-龥]"
        matchOB = re.match(pattern, origin)

        # originが空のとき、漢字以外の時はふりがなを振る必要がないのでそのまま出力する
        if origin != "" and matchOB:
            origin, kana, okurigana = kanadelete(origin, kana)
            text_new.append("{0}({1})".format(origin, kana)+okurigana)
        else:
            text_new.append(origin)
        node = node.next

    text_new = ''.join(text_new)
    return text_new
