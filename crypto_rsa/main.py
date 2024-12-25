import zipfile
import os.path
import os
from pathlib import Path
import sys

from decryptor_logic import decryptor


def traverse_extract_all():
    for dir, _, file_name in os.walk(enc_data_root_dir):
        for file in file_name:
            if file.endswith(".enc"):

                enc_abspath = os.path.join(dir, file)
                print(enc_abspath)
                tmpdir_without_ext = f"{os.path.splitext(enc_abspath)[0]}_tmp"
                print(tmpdir_without_ext)
                try:
                    os.mkdir(tmpdir_without_ext)
                except FileExistsError:
                    pass

                try:
                    with zipfile.ZipFile(enc_abspath, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir_without_ext)
                    # 解密data.enc -> data, 解密后得到的data文件是压缩文件
                    decryptor(tmpdir_without_ext)

                    data_file = os.path.join(tmpdir_without_ext, "data")
                    data_dir = os.path.join(tmpdir_without_ext, "data_dir").replace("\\2024\\", "\\2024_output\\")
                    with zipfile.ZipFile(data_file, 'r') as zip_ref:
                        zip_ref.extractall(data_dir)
                except:
                    pass


if __name__ == "__main__":
    enc_data_root_dir = os.path.join(Path(os.path.abspath(sys.argv[0])).parent.parent, "2024")
    traverse_extract_all()
