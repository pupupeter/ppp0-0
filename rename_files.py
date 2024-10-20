import os
import re

directory = os.path.expanduser('~/Desktop/ai批改/code') #修改為本地儲存作業的路徑

#用來檢查是否有(1),(2)等結尾的檔名
bracket_pattern = re.compile(r'^(.*)\s\((\d+)\)\.py$')

for filename in os.listdir(directory):
    if filename.endswith('.py'):
        parts = filename.split('_')

        #將檔案名稱分割
        if len(parts) >= 3:
            school_name = parts[0]  
            student_id = parts[1]  
            name = parts[2].split(' - ')[0]  

            #新檔名格式
            new_filename = f"{school_name}_{student_id}_{name}.py"

            match = bracket_pattern.match(filename)
            if match:
                #提取原本的檔名部分與括號中的數字
                base_name = match.group(1)
                number = match.group(2)
                new_filename = f"{base_name}_{number}.py"

            #檢查檔名是否需要修改
            if filename != new_filename:
                if not new_filename.startswith(filename):
                    counter = 1
                    original_new_filename = new_filename

                    while os.path.exists(os.path.join(directory, new_filename)):
                        new_filename = f"{original_new_filename[:-3]}_{counter}.py"
                        counter += 1

                    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                    print(f"重新命名: {filename} -> {new_filename}")

print("文件名稱修改成功!")
