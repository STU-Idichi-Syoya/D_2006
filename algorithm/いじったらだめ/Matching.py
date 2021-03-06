import sys,os
sys.path.append(os.path.dirname(__file__))
import CaboCha
import Parsing
import classes
# import Analize
import Analyze2 as Analize

import Proofreading
            

def virtual_server(sentence):   #サーバ側での動作をシュミレートしている

#--------------------------------------------
#必要なデータの収集
#--------------------------------------------
    res_file = Parsing.parsing(sentence)   #文書の解析を実行
    dic_file = open(os.path.dirname(os.path.abspath(__file__))+'/e-words2.txt')    #マッチングファイルの読み込み
    dic_data = dic_file.read()  #分けられていない辞書データ

    
#--------------------------------------------
#解析結果をまとめ上げる
#--------------------------------------------
    tr = load_tree(res_file)

#--------------------------------------------
#文書の解析を行う
#--------------------------------------------
    Analyzed_result = Analize.analyze(tr)

#--------------------------------------------
#まとめ上げられた物から名詞のみ取り出す
#--------------------------------------------
    nouns = extract_nouns(tr)
    #print("nouns:",nouns)
    #print()
    #print()

#--------------------------------------------
#IT用語集と照合
#--------------------------------------------
    detection = matching(nouns, dic_data)       #マッチング関数の実行
    #print("detection:",detection)
    #print()
    #print()

#--------------------------------------------
#前処理
#--------------------------------------------
    mark_word = Make_mark_word(detection)
    #print("markword:",mark_word)
    #print()
    #print()
 
#--------------------------------------------
#検知結果の部分の{}を付加する
#--------------------------------------------
    result_sentence = Mark(mark_word, sentence)     #マッチングした文字に{}で印をつける
    #print("result:",result_sentence)
    
#--------------------------------------------
#文書の校正
#--------------------------------------------
    result_sentence = Proofreading.proofreading(result_sentence)
    #print("result:",result_sentence)

#--------------------------------------------
#後掃除
#--------------------------------------------
    dic_file.close()               #ファイルのクローズ
    #print(result_sentence ,Analyzed_result)
    
    #先に難しい単語を抽出した文を返す(list型)
    #二個目に要点をまとめた文を返す(string型)
    return mark_word ,Analyzed_result


def load_tree(res_file):
    tr = classes.Tree()
    res_file= res_file.splitlines()
    for res in res_file:
        #print(res)
        if res[0:3] == 'EOS':   #ファイルの終端を検知
            break
        elif res[0] == '*':     #新しいchunkを追加
            tr.add_chunk(res[2:])
        else:
            tr.add_token(res)   #新しい単語を追加
    return tr


def extract_nouns(tr):
    combine_num, combine_str, combine_list, count = -2, "", [], -1
    nouns = []  #名詞の単語を集める
    for i, word in enumerate(tr.token_list):  #単語集を走破
        if word.surface == "接頭詞":
            #print(combine_num, combine_str, combine_list, word.text)
            nouns.append([combine_str, combine_list])   #それまで連続していた名詞達を結合した物をリストに保存
            count += 1
            combine_str = word.text    #文字列を結合
            combine_list = [count]  #結合した文字のインデックスを保存
            nouns.append([word.text, [count]])   #名詞ならリストに追加
            combine_num = i
                
        elif word.surface == "名詞":  #名詞かどうかを判定
            count += 1  #カウンタを加算
            if i == combine_num+1:  #一つ前のcombine_numと一致(前回検知した名詞から連続している)
                if combine_str == '':   #一つ前の名詞を追加する
                    combine_str += nouns[-1][0]     #名詞を結合
                    combine_list.append(count-1)    #番号を保存(nounsリスト内のインデックスとなる)
                combine_str += word.text    #文字列を結合
                combine_list.append(count)  #結合した文字のインデックスを保存
                #print('conbine')
            elif combine_str != '':     #連続していた名詞列が途切れたら
                nouns.append([combine_str, combine_list])   #それまで連続していた名詞達を結合した物をリストに保存
                #print(combine_str)
                combine_str = ''    #結合文字列を初期化
                combine_list = []   #結合も文字列リストを初期化
                
            combine_num = i     #nounsリスト内でのインデックスを保存
            nouns.append([word.text, [count]])   #名詞ならリストに追加
            #print([word.text, count])
        #print(combine_num, combine_str, combine_list)
            
    if combine_str != '':   #最後に結合文字列リスト内に残っている結合文字列を保存
        nouns.append([combine_str, [combine_list]])
        #print(combine_str)
    return nouns


def matching(nouns, data):  #マッチング処理
    detection, Severity = [], 2     #detection:検知された名詞の中でも特に難しいと判断された文字列のリスト, Severity: 名詞の閾値調整に使う
    data_sep = data.split()     #分けられた辞書リスト
    
    for word in nouns:  #検知された全ての名詞について調べる
        judge_score = float(len(word[1]))   #閾値の設定
        if len(word[0]) <= 4:
            continue
        #print(word[0], judge_score)
        score = 0.0     #スコアの初期化
        if judge_score > 1:     #もしword[0]が結合後の文字列だったら
            for index in word[1]:   #全ての結合文字列達の出現個数によって評価値を計算する
                #score += data.count(nouns[index][0])
                score += calc_rate(data.count(nouns[index][0]), Severity)   #出現数が多いほど評価が高い
                #print (calc_rate(data.count(nouns[index][0]), Severity))
        if word[0] in data_sep:     #もしword[0]がそのまま出現したら
            score += judge_score    #スコアが一気に閾値まで上がる
        #print(score)
        if score >= judge_score:    #閾値を超えていたら
            detection.append(word[0])   #リストに追加
            
    return detection


def calc_rate(match, param):   #評価値を計算する
    rate = 0.0
    for i in range(match):
        rate += 1/(param*(i+1))     #分数関数状にスコアがたまりにくくなる
        #print("rate: ", rate)
    return rate


def Make_mark_word(detection):
    mark_word = set()
    target_word = ''
    for word in reversed(detection):
        if word not in target_word:
            mark_word.add(word)
            target_word = word

    mark_word = sorted(mark_word, key=len, reverse=True) 
    #print("markword(bef): ",mark_word)
    return mark_word


def Mark(detection, sentence):
    for word in detection:
        #print(word)
        length = len(word)
        location = 0
        start = 0   #検索開始位置を保存
        while location > -1:
            location = sentence.find(word, start)
            #print(location)
            start = location + length
            if location != -1:
                sentence = insert_string_to_base(sentence, location, '{')
                sentence = insert_string_to_base(sentence, location+length+1, '}')
                start += 2
                #print(sentence)
    return sentence

def insert_string_to_base(target_string, insert_point, insert_string):
    return target_string[:insert_point] + insert_string + target_string[insert_point:]


def virtual_input():    #サーバー側での文字の受信をシュミレートしている
    #return "12行目において変数Aは機械の処理能力を測るために定義されている"
    #return "関数Bは変数Aの値によって処理内容が変わる"
    #return "関数Cは一つの文字列の内容に応じてTrueかFalseを返します"
    #return "関数Dは変数Aと変数Bをうけとり足し算を行った後で結果を返します"
    #return "送信ボタンはクリックされると、JSON形式でUserがしゃべった言葉をサーバへ送信する処理が行われる"
    #return "クラスEは関数Cの結果を保持する変数Aと関数Dの結果を保持する変数Bをメンバに持つ"
    #return "関数Fは内部で処理が分割されており変数Bの値によって切り替わる"
    #return "ハードウェアについては演算処理装置の高速化や搭載量の拡大や演算時のメモリ搭載量の大容量化や高速化や演算処理装置間でのメモリ共有方式が特徴的である他にベクトル計算に特有の演算処理装置を備える等取り扱われる演算に特有のハードウエア方式が採用されることがあるまた高い計算能力は演算処理を担う電子回路の大規模高速なスイッチング動作により実現されるため大量の電力消費と発熱に対応した電源設備や排熱冷却機構が必要である"
    return "ハードウェアについては、演算処理装置の高速化や搭載量の拡大、演算時のメモリ搭載量の大容量化・高速化、演算処理装置間でのメモリ共有方式が特徴的である。他にベクトル計算に特有の演算処理装置を備える等、取り扱われる演算に特有のハードウエア方式が採用されることがある。 また高い計算能力は演算処理を担う電子回路の大規模・高速なスイッチング動作により実現されるため、大量の電力消費と発熱に対応した電源設備、排熱・冷却機構が必要である。abstractクラス"
    #return "アジャイル開発はエンジニアを幸せにするためにある。"   #受信した文字を変えす

if __name__ == "__main__":
    sentence = virtual_input()  #文字の受信
    virtual_server(sentence)
    
