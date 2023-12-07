import os
import zipfile
from tqdm import tqdm

base_dir = "./zipfiles"
output_dir = "./unzipfiles"

if not os.path.isdir(output_dir):
    os.makedirs(output_dir, 0o777)

for i in tqdm(range(1,57)):
    final_path = os.path.join(base_dir,f"Images_png_{str(i).zfill(2)}.zip")
    os.system("unzip "+final_path+" -d "+output_dir)