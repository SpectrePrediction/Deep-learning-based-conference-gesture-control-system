import os

if __name__ == "__main__":
    # 存放20bn的文件路径
    root_path = r"D:\手势会议控制\20bn"
    # 20bn的前文件名
    bn_name = r"20bn-jester-v1-"
    # 合并后的文件名,这里我用的没有后缀,需要手动加，比如gzip、tar等
    cat_file_path = r"\20bn-jester-v1"

    dir_list = os.listdir(root_path)

    bn_path_list = [name for name in dir_list if (name.find(bn_name) != -1 and name.find(".") == -1)]

    bn_path_list = sorted(bn_path_list, key=lambda x: int(x.split("-")[-1]))

    # print(bn_path_list)

    with open(root_path + cat_file_path, "wb+") as cat_file:
        
        for bn_file_path in bn_path_list:
            path = root_path + "\\" + bn_file_path
            print(path)
            bn_file = open(path, "rb+")           
            cat_file.write(bn_file.read())
            bn_file.close()
    
    print("一帆风顺")

