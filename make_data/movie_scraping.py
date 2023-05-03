'''from pytube import YouTube

# 動画をダウンロードしたいYouTubeのURLを指定します
url = "https://www.youtube.com/watch?v=7szNRrs5H3c&t=1670s&ab_channel=KENのスマブラ配信"

# # YouTubeオブジェクトを作成し、ストリームをフィルタリングして、最高品質の動画を取得します
youtube = YouTube(url)
# video = youtube.streams.get_highest_resolution()

# # 動画をダウンロードし、指定したパスに保存します
# video.download('C:/Users/Kimac/Desktop/working/ポートフォリオ/ssbu_machine_learning/movie')

from tqdm import tqdm
import time

# for i in tqdm(video.download('C:/Users/Kimac/Desktop/working/ポートフォリオ/ssbu_machine_learning/movie')):
#     time.sleep(1) # 1秒待機
    
video = youtube.streams.get_highest_resolution()
filesize = video.filesize # ファイルサイズを取得
with tqdm(total=filesize, unit='B', unit_scale=True, desc=youtube.title) as pbar:
    video.download(output_path="./", filename=youtube.title, 
                   on_progress=lambda stream, chunk, bytes_remaining: 
                   pbar.update(filesize - bytes_remaining))
'''


from pytube import YouTube

url = "https://youtu.be/RTlHUvMnVXM"
YouTube(url).streams.get_highest_resolution().download()


# from pytube import YouTube

# # 動画をダウンロードしたいYouTubeのURLを指定します
# url = "https://www.youtube.com/watch?v=RTlHUvMnVXM&ab_channel=Tamisuma.jp"

# # YouTubeオブジェクトを作成し、ストリームをフィルタリングして、最高品質の動画を取得します
# youtube = YouTube(url)
# video = youtube.streams.get_highest_resolution()

# # 動画をダウンロードし、指定したパスに保存します
# video.download('make_data/movie')





# from pytube import YouTube
# from tqdm import tqdm

# # 動画をダウンロードしたいYouTubeのURLを指定します
# url = "https://www.youtube.com/watch?v=7szNRrs5H3c&t=1670s&ab_channel=KENのスマブラ配信"

# # YouTubeオブジェクトを作成し、ストリームをフィルタリングして、最高品質の動画を取得します
# youtube = YouTube(url)
# video = youtube.streams.get_highest_resolution()

# # ダウンロード時にプログレスバーを表示するための関数
# def progress_function(stream, chunk, bytes_remaining):
#     current = video.filesize - bytes_remaining
#     progress = (current / video.filesize) * 100
#     bar.update(progress)

# # プログレスバーを初期化
# bar = tqdm(total=100, unit='%', desc="Downloading", ncols=100)

# # プログレスバーの表示を更新するための関数を登録
# youtube.register_on_progress_callback(progress_function)

# # 動画をダウンロードし、指定したパスに保存します
# video.download('C:/Users/Kimac/Desktop/working/ポートフォリオ/ssbu_machine_learning/movie')

# # プログレスバーを終了
# bar.close()
