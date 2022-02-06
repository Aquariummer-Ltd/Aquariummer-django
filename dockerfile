# python:3.7-alpineイメージを指定
FROM python:3.10-alpine

# プロジェクトの管理者を記載
LABEL maintainer = "Aquariummer.Ltd <keita.ide78dev@gmail.com>"

# 標準出力に出力されるバッファを無効化
ENV PYTHONUNBUFFERED 1

# txtファイルをイメージ側のappディレクトリに配置
COPY ./requirements.txt /requirements.txt

# pipコマンドを最新にし、txtファイル内のパッケージをインストール
RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2

# ローカルのapp配下のファイルをイメージ側のapp配下にコピー
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# "user"ユーザを作成し実行ユーザを変更する
RUN adduser -D user
USER user
