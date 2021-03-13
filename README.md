# OpenHackU_vol_4_ID15
焼肉焼いたら家焼けたbot  
  
「焼肉焼いたら家焼けたbot」はヤフー株式会社主催のイベント「Hack U」にて企画・開発を行った言葉遊びbotです。  
  
- [遊び方ガイド ](https://note.com/roast_official/n/ndc7d00f38d44)  
  
  
----------------------------------------------------------------------

## 環境設定  
- ディレクトリ構成  
├── main.py(channelIDなどはherokuの環境変数としておいている)  
├── runtime.txt(Pythonのバージョンを記載)  
├── requirements.txt(依存するライブラリの記載)  
├── Procfile(プログラムの実行方法を定義)  
├── .env  
├── .gitignore  
  
## 環境変数の設定  
```$ heroku config:set YOUR_CHANNEL_SECRET="Channel Secretの文字列" --app アプリ名```  
```$ heroku config:set YOUR_CHANNEL_ACCESS_TOKEN="アクセストークンの文字列" --app アプリ名```  

- 補足 Herokuにデプロイ後、Config Varsで設定するのでもOK  
  
## 新しい Heroku アプリの作成  
```$ heroku create アプリ名```  
- アプリ名を無記入にした場合は自動で作成される  
- リネームは ```$ heroku rename 新しい名前 --app 古い名前```  
  
## デプロイ  
- (個人の)メインブランチにデプロイ  
```$ git push heroku master```  
- 共用リボジトリの個人用ブランチから、herokuのmasterにデプロイする  
```git push heroku ブランチの名前:master --force```  
**Herokuにはmasterにデプロイしなければ、remote: Pushed to non-master branch, skipping build.というbuild errorになる**
  
```
Username for 'https://github.com': メールアドレス  
Password for 'https://yud0uhu@github.com': <b>AccountにあるAPI Key</b>  
```
  
GitHubに(個人用ブランチを切って)pushする  
```$ git checkout -b ブランチ名```  
```$ git push origin ブランチ名```  
  
##エラー対処  
```git push heroku```で  
```$ \linebot>git push heroku```  
```fatal: 'heroku' does not appear to be a git repository```  
```fatal: Could not read from remote repository.```  
 
```
Please make sure you have the correct access rights  
and the repository exists.  
```
のエラーが出たときは、  
  
```$ git remote add heroku https://git.heroku.com/アプリ名.git```  

## アクセスログの確認
```$ heroku logs```  
  
## 参考/LINE DevelopesのWebhook URLの接続確認でエラーが出る件について  
https://qiita.com/q_masa/items/c9db3e8396fb62cc64ed  
  
## 参考/デプロイ系  
https://uepon.hatenadiary.com/entry/2018/07/27/002843  
https://qiita.com/shimajiri/items/cf7ccf69d184fdb2fb26#flask%E3%81%A8line-bot-sdk%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB  
https://devcenter.heroku.com/ja/articles/git (Heroku公式/Gitを使用したデプロイ)  
  
## 公式SDK  
https://github.com/line/line-bot-sdk-python  
  
## 自分用メモ
- (WSL)herokuコマンドには**sudo**が必要  
- http://smot93516.hatenablog.jp/entry/2018/10/09/115933  
- https://reasonable-code.com/heroku-config/ (Herokuで環境変数を確認・設定・削除する方法)  
