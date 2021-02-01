import csv
import os
import shutil
from queue import Queue
import threading


def log_print(*args, **kwargs):
    print("\033[0;31m[log:\033[0m", *args, "\033[0;31m]\033[0m", **kwargs)


def get_default_white_list(label_csv_path: str) -> list:
    """
    得到默认白名单
    :param label_csv_path: 标签csv地址
    :return: 白名单 list类型
    """

    return [x[0] for x in read_csv(label_csv_path)]


def read_csv(path: str, mode: str="r") -> csv.reader:
    """
    读取csv 并返回一个csv.reader类型
    :param path: 读取地址
    :param mode: 读取模式
    :return: csv.reader类型
    """
    f_read = open(path, mode)
    f_reader = csv.reader(f_read)

    return f_reader


def collation_and_move(jester_root_path: str, output_root_path: str, jester_list: list,
                       white_list: list, mode: str="copy", strict: bool=True) -> None:
    """
    整理jester数据集
    将同一类的所有文件移动到对应类别标签文件夹下
    :param jester_root_path: jester数据集文件的跟目录
    :param output_root_path: 保存整理后类别文件的根目录
    :param jester_list: jester信息列表，使用jester-v1-train/test/validation.csv类别
    :param white_list: 白名单，指定类别，不在白名单中的类别文件不会移动
    :param mode: 模式,支持move和copy, 默认是copy
    注： copy: 复制根目录下的文件并移动到output目录，原目录下文件保存不变
        move： 直接移动根目录下的文件到output目录，原目录消失
    :param strict:是否严格？默认是True
    注：True：需要jester_list中所有文件对应存在，一旦有文件找不到即抛出异常
        False：不讲究，仅对已有的文件进行操作，找不到对应文件即跳过
    :return:None
    """

    mode_func_dict = {
        "copy": shutil.copytree,
        "move": os.renames  # shutil.move
    }

    mode_func = mode_func_dict.get(mode, None)
    if not mode_func:
        raise TypeError(f"输入mode为{mode},但mode仅支持{mode_func_dict.keys()}")
    log_print(f"使用模式为 {mode}, 严格的？{strict}")

    for jester_inf_str in jester_list:
        name, labels = jester_inf_str.split(";")

        if not white_list.count(labels):
            # log_print(f"跳过: {name} 标签{labels}不在白名单")
            continue

        name_path = os.path.join(jester_root_path, name)

        if not os.path.exists(name_path):
            if strict:
                raise FileNotFoundError(f"他应当存在但找不到此地址 {name_path}, labels: {labels}")
            continue

        output_label_dir = os.path.join(output_root_path, labels)
        if not os.path.exists(output_label_dir):
            os.makedirs(output_label_dir)

        out_name_path = os.path.join(output_label_dir, name)
        log_print(f"正在处理: {name_path} 变更为 {out_name_path}")
        mode_func(name_path, out_name_path)

    log_print("一帆风顺", end="\n\n")


def thread_collation_and_move(jester_root_path: str, output_root_path: str, jester_list: list,
                              white_list: list, mode: str="copy", strict: bool=True, thread_num: int=32) -> None:
    """
    使用线程 整理jester数据集
    将同一类的所有文件移动到对应类别标签文件夹下
    :param jester_root_path: jester数据集文件的跟目录
    :param output_root_path: 保存整理后类别文件的根目录
    :param jester_list: jester信息列表，使用jester-v1-train/test/validation.csv类别
    :param white_list: 白名单，指定类别，不在白名单中的类别文件不会移动
    :param mode: 模式,支持move和copy, 默认是copy
    注： copy: 复制根目录下的文件并移动到output目录，原目录下文件保存不变
        move： 直接移动根目录下的文件到output目录，原目录消失
    :param strict:是否严格？默认是True
    注：True：需要jester_list中所有文件对应存在，一旦有文件找不到即抛出异常
        False：不讲究，仅对已有的文件进行操作，找不到对应文件即跳过
    :param thread_num: 线程数
    :return:None
    """

    mode_func_dict = {
        "copy": shutil.copytree,
        "move": os.renames  # shutil.move
    }

    mode_func = mode_func_dict.get(mode, None)
    if not mode_func:
        raise TypeError(f"输入mode为{mode},但mode仅支持{mode_func_dict.keys()}")
    log_print(f"使用模式为 {mode}, 严格的？{strict}")

    jester_queue = Queue()
    for jester_inf_str in jester_list:
        jester_queue.put(jester_inf_str)

    def thread_worker(jester_root_path: str, output_root_path: str, white_list: list, mode_func, strict: bool=True):
        while True:
            jester_inf_str = jester_queue.get()
            name, labels = jester_inf_str.split(";")

            if not white_list.count(labels):
                # log_print(f"跳过: {name} 标签{labels}不在白名单")
                continue

            name_path = os.path.join(jester_root_path, name)

            if not os.path.exists(name_path):
                if strict:
                    raise FileNotFoundError(f"他应当存在但找不到此地址 {name_path}, labels: {labels}")
                continue

            output_label_dir = os.path.join(output_root_path, labels)
            if not os.path.exists(output_label_dir):
                os.makedirs(output_label_dir)

            out_name_path = os.path.join(output_label_dir, name)
            log_print(f"正在处理: {name_path} 变更为 {out_name_path}")
            mode_func(name_path, out_name_path)

    for i in range(thread_num):
        worker = threading.Thread(target=thread_worker, args=(jester_root_path, output_root_path,
                                                     white_list, mode_func, strict))
        worker.setDaemon(True)
        worker.start()

    while not jester_queue.empty():
        pass

    log_print("一帆风顺", end="\n\n")


if __name__ == '__main__':
    train_path = "jester-v1-train.csv"
    labels_path = "jester-v1-labels.csv"

    # 读取训练csv
    train_jester_list = [x[0] for x in read_csv(train_path)]

    # 获取默认白名单，默认即是全部
    # white_list = get_default_white_list(labels_path)
    # 自己设定白名单，不在白名单中的类别不会受到影响
    white_list = [
        "Doing other things",
        "No gesture",
        "Stop Sign",
        "Zooming In With Full Hand",
        "Zooming Out With Full Hand",
        "Drumming Fingers",
        "Swiping Left",
        "Swiping Right",
    ]
    # collation_and_move(
    #     "20bn",
    #     "20bncollation",
    #     train_jester_list,
    #     white_list,
    #     "copy",
    #     True
    # )
    thread_collation_and_move(
        "20bn",
        "20bncollation",
        train_jester_list,
        white_list,
        "copy",
        False
    )

