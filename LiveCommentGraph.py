import pytchat
from datetime import datetime
import matplotlib.pyplot as plt
import re

def get_video_id(url):
    # URLからvideo_idを抽出
    video_id_match = re.search(r'v=([A-Za-z0-9_-]+)|/live/([A-Za-z0-9_-]+)', url)
    if video_id_match:
        return video_id_match.group(1) or video_id_match.group(2)
    return None

def main():
    url = input("YouTubeの配信のURLを入力: ")
    video_id = get_video_id(url)

    if video_id:
        livechat = pytchat.create(video_id=video_id)

        # キーワードをユーザーから入力
        raw_keywords = input("抜粋したいキーワードをカンマで区切って入力 (未指定の場合はEnterキーを押してください): ")
        keywords = raw_keywords.split(",") if raw_keywords else []
 
        print("処理中...")

        # キーワードごとのコメントカウントを格納する辞書
        keyword_counts = {keyword: [] for keyword in keywords}

        # 全コメントのカウント
        all_comments = []

        first_comment = True  # 最初のコメントを判定するフラグ
        start_time = None  # 最初のコメントの時刻を保存する変数

        while livechat.is_alive():
            chatdata = livechat.get()
            for c in chatdata.items:
                # コメントの内容を取得
                comment = c.message
                if first_comment:
                    # 最初のコメントの時刻を取得
                    start_time = datetime.fromisoformat(c.datetime)
                    first_comment = False  # 最初のコメントの時刻が取得されたらフラグをオフにする

                # 全コメントの時間をカウント
                elapsed_time = (datetime.fromisoformat(c.datetime) - start_time).total_seconds() / 60
                all_comments.append(elapsed_time)

                # キーワードごとのコメントカウント
                for keyword in keywords:
                    if keyword.startswith('"') and keyword.endswith('"'):
                        # キーワードがダブルクオーテーションで囲まれている場合
                        if keyword[1:-1] == comment:
                            keyword_counts[keyword].append(elapsed_time)
                    elif keyword in comment:
                        keyword_counts[keyword].append(elapsed_time)

        # グラフを描画
        plt.figure(figsize=(12, 6))  # グラフのサイズを設定
        for keyword, times in keyword_counts.items():
            if times:  # キーワードごとのコメントが存在する場合のみヒストグラムを描画
                plt.hist(times, bins=range(0, int(max(times)) + 2, 1), alpha=0.5, label=keyword)

        if not keywords:  # 全コメントのリストが空でないことを確認
            # 全コメントの頻度を描画
            plt.hist(all_comments, bins=range(0, int(max(all_comments)) + 2, 1), alpha=0.5, label="全コメント")
               
        print("完了！")

        plt.xlabel("時間 (分)",fontname="MS Gothic")
        plt.ylabel("コメントの頻度",fontname="MS Gothic")
        plt.legend(prop={"family":"MS Gothic"})
        plt.title("キーワードごとのコメント頻度",fontname="MS Gothic")
        plt.xticks(range(0, int(max(all_comments)) + 2, 10))  # 横軸の目盛りを設定
        plt.show()

    else:
        print("URLからvideo_idを抽出できませんでした。正しいURLを入力してください.")

if __name__ == "__main__":
    main()
