import glob
import os
from google.colab import drive
from pydub import AudioSegment

# Google Driveをマウント
drive.mount('/content/drive')

# 必要なライブラリをインストール
!pip install pydub

# pydubをインポート
from pydub.silence import split_on_silence

# 入力ディレクトリと出力ディレクトリを指定
input_dir = '/content/drive/MyDrive/samples/long'
output_dir = '/content/drive/MyDrive/samples'

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 入力ディレクトリ内の音声ファイルを取得
input_files = glob.glob(os.path.join(input_dir, '*.wav'))

# 音声ファイルの波形から話している部分を検出し、ぶつ切りにして保存
for input_file in input_files:
    # 音声ファイルを読み込み
    audio = AudioSegment.from_wav(input_file)

    # 無音部分で音声を分割
    silence_ranges = split_on_silence(audio, silence_thresh=-40, min_silence_len=500)

    # 検出した無音部分から話している部分を切り出し、保存
    for i, silence_range in enumerate(silence_ranges):
        # 部分音声を切り出し
        segment = silence_range

        # 出力ファイル名を作成
        output_file = os.path.join(output_dir, f'{os.path.basename(input_file)}_{i + 1}.wav')

        # 出力ファイルが既に存在する場合、適切なファイル名を生成
        if os.path.exists(output_file):
            base, ext = os.path.splitext(output_file)
            output_file = f'{base}_{i + 1}{ext}'

        # 部分音声を保存
        segment.export(output_file, format="wav")

print("処理が完了しました。")
