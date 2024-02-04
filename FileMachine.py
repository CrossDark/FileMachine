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
                print(1)
                os.symlink(os.path.join(sets[1], item_name), item_name)


def projects(settings_list):
    """
    处理方法:将位于不同位置的文件夹集中到当前目录下
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


def lists():
    pass


def exec_(get_dir):
    cleanup_symlinks()
    if get_dir[0][0] == 'mode':
        if get_dir[0][1] == 'storage':
            storage(get_dir[1:])
        elif get_dir[0][1] == 'working':
            projects(get_dir[1:])
    else:
        print('请设置一种模式')


def main():
    """# 尝试读取目录列表
        try:
            for dirs in read():
                # 切换到脚本所在的目录，以防在其它地方执行此脚本
                os.chdir(os.path.dirname(os.path.abspath(dirs)))
                # 清理之前的符号链接
                cleanup_symlinks()
                # 创建链接
                storage(settings_list)
                # 输出结果
                print('"', os.path.basename(os.path.dirname(dirs)), '"', '执行成功')
        except FileNotFoundError:
            # 切换到脚本所在的目录，以防在其它地方执行此脚本
            # os.chdir(os.path.dirname(os.path.abspath(dirs)))
            # 清理之前的符号链接
            cleanup_symlinks()
            # 创建链接
            projects(settings_list)
"""
    exec_(read_dirs('settings.txt'))


if __name__ == '__main__':
    main()
    