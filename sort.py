from pathlib import Path
import shutil
import sys
import os
import re


print(sys.argv)
try:
    path = Path(sys.argv[1])
    print (path.exists())

except IndexError as e:
    print('you ahould writ path')    



known_ext = {'audios':['.mp3', '.wma', '.ogg'], 'images':['.png', '.jpg', '.jpeg'],
 'documents':['.doc', '.docx', '.txt', '.xlsx', '.pptx'], 
 'video':['.avi', '.mp4', '.mov', '.mkv'], 'archives':['.zip', '.gz', '.tar', '.rar'], 'unknown':[]}



list_of_known_ext = []
list_of_unknown_ext = []


list_sorted = {'audios':[], 'images':[], 'documents':[], 'video':[], 'archives':[], 'unknown':[]}


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    
    TRANS = {}
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
      TRANS[ord(c)] = t
      TRANS[ord(c.upper())] = t.upper()

    pre_norm_file_name = file_name.translate(TRANS)      
    
    pre_norm_file_name_split = re.split('\.', pre_norm_file_name)    
    
    norm_file_name_0 = ''

    for i in pre_norm_file_name_split[0]:      
        p = re.sub('\W', '_', i)
 
        norm_file_name_0 += p

    norm_file_name = f'{norm_file_name_0}.{pre_norm_file_name_split[1]}'

    return norm_file_name


def sort(path, global_path=path):
    path = Path(path)
    
    for i in path.iterdir():         
        file_name = i.name

        if i.is_file():               
            
            file_name = Path(file_name)
            s = file_name.suffix.replace('.', '')
            file_class = False

            for k, v in known_ext.items():        

                if file_name.suffix in v:
                    list_sorted.update({k: normalize(file_name.name)})            
                    list_of_known_ext.append(s)            
                    file_class = True

                    dir_name = k

            if file_class == False:
                list_sorted.update({'unknown': normalize(file_name.name)})
                list_of_unknown_ext.append(s)
                
                dir_name = 'unknown'      
          
            new_dir = Path(os.path.join(global_path, dir_name))
            
            new_dir.mkdir(exist_ok = True, parents = True)
            
            shutil.move(os.path.join(path, file_name), new_dir)


        elif i.is_dir():
            sort(i)
            if not os.listdir(i):    #якщо папка пуста - видаляємо 
                i.rmdir()

    for i in global_path.iterdir():
        if i.name == 'archives':
            for j in i.iterdir():
                shutil.unpack_archive(j, i)


    print (f'list_sorted = {list_sorted}')
    print (f'list_of_known_ext = {list_of_known_ext}')
    print (f'list_of_unknown_ext = {list_of_unknown_ext}')

__name__=="__main__" 

#python Git\hw6_py12\sort.py C:/Users/user/Desktop/GoIT_Phyton/HW6/Motloh
sort(path)