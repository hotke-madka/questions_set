import tkinter as tk
from tkinter import filedialog,simpledialog
import os
import cv2
import shutil
import numpy as np

def crop_and_save_regions(image, regions, output_path, image_id):
    """
    複数の領域を切り分けて保存する関数
    """
    for i, region in enumerate(regions):
        x, y, w, h = region  # 領域の座標を取得
        cropped_image = image[y:y+h, x:x+w]  # 指定した領域を切り分け
        output_filename = f"{output_path}/{image_id}_reg{i+1:03d}.jpg"  # 保存するファイル名
        cv2.imwrite(output_filename, cropped_image)  # 画像を保存

def process_image(image_path, output_path, image_id):
    """
    画像の読み込みと切り抜き処理を行う関数
    """
    
    print(f"Processing {image_path}")
    # 画像の読み込み
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    # 指定する領域のリスト
    regions = [
        (60, 220, 650, 50),   
        (710, 220,500, 50),  
        (60, 270, 1200, 50),
        (60,320,1200,50),
        (60,360,560,50),#5
        (620,360,560,50),
        (60,400,1200,50),
        (60,490,1200,70),
        (60,550,1200,70),
        (60,700,580,90),#10
        (60,780,580,90),
        (60,860,580,90),
        (60,940,580,90),
        (60,1000,580,90),#15
        (60,1080,580,90),
        (60,1150,580,90),
        (60,1200,580,90)
    ]
    
    
    # 元の画像をコピーして保存 (original_imageフォルダに保存)
    original_output_path = os.path.join(output_path, "original_image")
    os.makedirs(original_output_path, exist_ok=True)
    original_filename = f"{original_output_path}/{image_id}_original.jpg"
    shutil.copy(image_path, original_filename)
    
    # 切り分けて保存 (question_imageフォルダに保存)
    question_output_path = os.path.join(output_path, "question_image")
    os.makedirs(question_output_path, exist_ok=True)
    crop_and_save_regions(image, regions, question_output_path, image_id)

def select_folder():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しないようにする
    folder_path = filedialog.askdirectory(title="フォルダを選んでね")  # フォルダ選択ダイアログを表示
    return folder_path

def input_folder_name():
    root = tk.Tk()
    root.withdraw()
    folder_name = simpledialog.askstring("フォルダ名の入力", "新しいフォルダの名前を入力してください:")
    return folder_name

def main():
    # フォルダの選択
    input_folder = select_folder()
    if not input_folder:
        print("フォルダが選択されませんでした。プログラムを終了します。")
        return

    output_folder_base = input_folder_name()
    if not output_folder_base:
        print("フォルダ名が入力されませんでした。プログラムを終了します。")
        return
    
    # 出力先のフォルダのパス
    parent_dir = os.path.dirname(input_folder)
    output_folder = os.path.join(parent_dir, output_folder_base)
    
    # 出力先のフォルダが存在しない場合は作成する
    os.makedirs(output_folder, exist_ok=True)

    # フォルダ内のすべてのファイルをリストアップ
    files = os.listdir(input_folder)

    # 画像ファイルのみを選択し処理を行う
    for i, file in enumerate(files, start=1):
        # 画像ファイルであるかどうかを確認
        if file.endswith((".jpg", ".jpeg", ".png")):
            # 画像のパス
            image_path = os.path.join(input_folder, file)
            # ID (ファイル名を使用する例)
            image_id = f"id{i:03d}"
            # 処理を行う関数を呼び出す
            process_image(image_path, output_folder, image_id)

if __name__ == "__main__":
    main()
