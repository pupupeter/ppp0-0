import os
import subprocess
import shutil
import re

non_py_dir = './code/non_py_files'
format_error_dir = './code/format_error'
os.makedirs(non_py_dir, exist_ok=True)
os.makedirs(format_error_dir, exist_ok=True)

#正則表示式，允許名稱帶有後綴的檔案，如：學校名稱_學號_姓名.py 或 學校名稱_學號_姓名_1.py
valid_pattern = re.compile(r'^[\u4e00-\u9fa5_a-zA-Z]+_\d+_[\u4e00-\u9fa5_a-zA-Z]+(_\d+)?\.py$')

files = [e for e in os.listdir('./code') if e.endswith('.py')]

#將非 .py 檔移到 non_py_files 資料夾
for e in os.listdir('./code'):
    if not e.endswith('.py') and e != 'non_py_files' and e != 'format_error':
        shutil.move(os.path.join('./code', e), os.path.join(non_py_dir, e))

#將檔名格式錯誤的檔案移到 format_error 資料夾
for file in files[:]:
    if not valid_pattern.match(file):
        shutil.move(os.path.join('./code', file), os.path.join(format_error_dir, file))
        files.remove(file)

f = open('score.csv', 'w', encoding='utf-8-sig')
f.write(','.join(['學校', '學號', '姓名', '分數', '編號']) + '\n')

for file in files:
    result = subprocess.run(['python', 'judge.py', './code/' + file], stdout=subprocess.PIPE)
    try:
        output = result.stdout.decode('utf-8')
    except:
        output = result.stdout.decode('cp950')
    
    print(file)
    print(output, end='')

    #分割檔名並檢查檔名是否有帶有 "_1", "_2" 等後綴
    file_parts = file[:-3].split('_')
    if file_parts[-1].isdigit():  
        r_data = file_parts[:-1] + [output.strip().split('\n')[-1], file_parts[-1]]
    else:
        r_data = file_parts + [output.strip().split('\n')[-1], '']  #沒有編號則留空
    
    print(r_data)
    print()
    f.write(','.join(r_data) + '\n')

f.close()
