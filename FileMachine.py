"""
文件处理
"""
import os


def read_dirs(file_path):
    """从给定的文件中读取目录列表，并返回一个目录名列表。"""
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')
        return [line.strip().split(' = ', 1) for line in lines if line.strip()]


def cleanup_symlinks():
    """删除当前目录下的所有符号链接。"""
    for item in os.listdir('.'):
        if os.path.islink(item):
            os.unlink(item)


def storage(settings_list):
    """
    处理方法:切换不同文件夹组到目录下
    设置方法:mode = filing
            path = 你选中的那组文件夹的父文件夹
    :param settings_list:
    :return:
    """
    for sets in settings_list:
        if not sets:
            continue
        if sets[0] == 'path':
            for item_name in os.listdir(os.path.abspath(sets[1])):
                # 跳过以'.'开头的隐藏文件和目录
                if item_name.startswith('.'):
                    continue
                # 创建符号链接
                os.symlink(os.path.join(sets[1], item_name), item_name)
            print('链接成功')
        else:
            print('请设置path语句')


def projects(settings_list):
    """
    处理方法:将位于不同位置的文件夹集中到当前目录下
    设置方法:mode = working
            <项目目录1> = <项目文件夹1><项目文件夹2>
            …………
    :param settings_list:
    :return:
    """
    for sets in settings_list:
        if not sets:
            continue
        if os.path.isdir(sets[0]):
            for v in sets[1].split(' '):
                if os.path.exists(os.path.join(sets[0], v)):
                    try:
                        os.symlink(os.path.join(sets[0], v), v)
                        print('"', v, '"', '执行成功')
                    except FileExistsError:
                        print('没有那个文件')
                else:
                    print('Wrong')
        else:
            print('该路径不是目录')


def lists():
    pass


def exec_(get_dir):
    """
    依据mode执行不同函数
    :param get_dir:
    :return:
    """
    cleanup_symlinks()
    if get_dir[0][0] == 'mode':
        mode = get_dir[0][1]
        if mode == 'filing':
            storage(get_dir[1:])
        elif mode == 'working':
            projects(get_dir[1:])
        elif mode == 'clean':
            pass
    else:
        print('请设置一种模式')


def main():
    exec_(read_dirs('settings.txt'))


if __name__ == '__main__':
    main()
    