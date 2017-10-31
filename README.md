# downloader
メインプログラム:downloader.py    
  モジュールプログラム:googledownload.py 、check.py    
別途必要モジュールのインストールが必要   
    
別途必要なソフトウェアのインストール方法        
  http://taku910.github.io/mecab/#download 　からmecab-0.996.exeをダウンロードし実行。    
  インストール時に 文字コード について聞かれるので、utf-8を選択。   

推奨する環境設定方法   
  anaconda python3.x をインストールしpathを設定。(現在での最新版は3.6、pathはインストール時に選択することで簡単に設定ができる)   
  cmd(コマンドプロンプト)で conda create -n myenv python=3.5.2 anaconda と入力(myenvという仮想環境が作成され、python3.5.2をmyenvにインストール)    
  cmd で python -m pip install モジュール名 で必要なモジュールをインストール。    
