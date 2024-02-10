"""
文件处理
"""
import os
import re


def read_settings(file_path):
    """
    从给定的文件中读取目录列表，并返回一个目录名列表。
    以以下顺序移除注释:
    1.移除所有被<>扩起来的内容以及<>本身
    2.移除所有#后一直到行末的字符
    3.移除所有以#开头的行
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        return [
            line.strip().split(' = ', 1)
            for line in re.sub(r'#.*\n', '\n', re.sub('<[^>]*>', '', file.read())).split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]


def make_settings(file_path):
    with open(file_path, 'w') as file:
        file.write('mode = clean')


def cleanup_symlinks():
    """删除当前目录下的所有符号链接。"""
    for item in os.listdir('.'):
        if os.path.islink(item):
            os.unlink(item)


def filing(settings_list):
    """
    处理方法:切换不同文件夹组到目录下
    设置方法:mode = filing
           <你选中的那组文件夹的父文件夹>(如果设置了多个父文件夹,请确保它们没有名称相同的子文件夹)
    :param settings_list:
    :return:
    """
    for sets in settings_list:
        if not sets:
            continue
        if os.path.isdir(sets[0]):
            for item_name in os.listdir(os.path.abspath(sets[0])):
                # 跳过以'.'开头的隐藏文件和目录
                if item_name.startswith('.'):
                    continue
                # 创建符号链接
                os.symlink(os.path.join(sets[0], item_name), item_name)
            print('链接成功')
        else:
            print('请设置path语句')


def working(settings_list):
    """
    处理方法:将位于不同位置的文件夹集中到当前目录下
    设置方法:mode = working
            <项目目录1> = <项目文件夹1> <项目文件夹2>
            …………
    :param settings_list:
    :return:
    """
    for sets in settings_list:
        if not sets:
            continue
        for v in sets[1].split(' '):
            if os.path.exists(os.path.join(sets[0], v)):
                try:
                    os.symlink(os.path.join(sets[0], v), v)
                    print('"', v, '"', '执行成功')
                except FileExistsError:
                    print('没有那个文件')
            else:
                print('Wrong')


def mix(settings_list):
    pass


def help_():
    pass


def lists():
    read_settings('list.txt')


def exec_(get_dir):
    """
    依据mode执行不同函数
    :param get_dir:
    :return:
    """
    cleanup_symlinks()
    if get_dir[0][0] == 'mode':
        mode = get_dir[0][1]
        settings = get_dir[1:]
        if mode == 'filing':
            filing(settings)
        elif mode == 'working':
            working(settings)
        elif mode == 'clean':
            pass
        elif mode == 'mix':
            mix(settings)
        elif mode == 'help':
            help_()

    else:
        print('请设置一种模式')


def main():
    try:
        exec_(read_settings('settings.txt'))
    except FileNotFoundError:
        make_settings('settings.txt')


if __name__ == '__main__':
    main()
