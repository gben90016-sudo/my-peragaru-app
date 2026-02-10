import streamlit as st
import yfinance as yf
import pandas as pd

# 1. アプリのタイトルを表示
st.title('俺のPERAGARU (ベータ版)')

# 2. ユーザーが銘柄コードを入力する場所を作る
ticker = st.text_input('銘柄コードを入力してください (例: 7203.T)', '7203.T')

# 3. 期間を選ぶスライダーを作る
days = st.slider('表示する期間（日数）', 30, 365, 180)

# 4. ボタンが押されたらデータを取得して表示
if st.button('分析開始'):
    try:
        # 株価データの取得
        df = yf.download(ticker, period=f'{days}d')
        
        # データが空の場合のチェック
        if df.empty:
            st.error("データが見つかりませんでした。銘柄コードを確認してください。")
        else:
            # 最新の終値を表示（ここを修正しました！）
            # .iloc[-1]で取得したデータが配列(Series)になっている場合に対応するため float() で数値に変換
            latest_price = float(df['Close'].iloc[-1])
            st.metric(label="現在の株価", value=f"{latest_price:,.1f} 円")

            # チャートを描く
            st.line_chart(df['Close'])

            # データの中身を表示
            st.write('詳細データ:')
            st.dataframe(df.tail())

    except Exception as e:
        st.error(f'エラーが発生しました: {e}')
        st.write('ヒント: 日本株の場合はコードの後に .T をつけてください（例: 7203.T）')
