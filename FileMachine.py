"""
文件处理
"""
import os
import re
import ruamel.yaml


def read_yaml(path):
    """
    读取yaml并移除被<>扩起来的注释
    :return:
    """
    with open(path, encoding='utf-8') as file:

        return ruamel.yaml.YAML(typ='safe').load(re.sub('<[^>]*>', '', file.read()))


def make_settings(file_path):
    """创建设置文件"""
    with open(file_path, 'w') as file:
        file.write('clean')


def cleanup_symlinks():
    """删除当前目录下的所有符号链接。"""
    for item in os.listdir('.'):
        if os.path.islink(item):
            os.unlink(item)


class Filing:
    def __init__(self, settings):
        """
        处理方法:切换不同文件夹组到目录下
        设置方法:mode = filing
               <你选中的那组文件夹的父文件夹>(如果设置了多个父文件夹,请确保它们没有名称相同的子文件夹)
        :param settings:
        :return:
        """
        if type(settings) == str:
            self.settings = settings.split(' ')
        elif type(settings) == list:
            self.settings = settings
        else:
            print('不支持dict')
            return
        self.list()

    def list(self):
        for sets in self.settings:
            if not sets:
                continue
            if os.path.isdir(sets):
                for item_name in os.listdir(os.path.abspath(sets)):
                    # 跳过以'.'开头的隐藏文件和目录
                    if item_name.startswith('.'):
                        continue
                    # 创建符号链接
                    os.symlink(os.path.join(sets, item_name), item_name)
                print('链接成功')
            else:
                print('请设置path语句')


class Working:
    def __init__(self, settings):
        """
        处理方法:将位于不同位置的文件夹集中到当前目录下
        设置方法:mode = working
                <项目目录1> = <项目文件夹1> <项目文件夹2>
                …………
        :param settings:
        :return:
        """
        for k, v in settings.items():
            self.keys = k
            self.values = v
            if type(v) == list:
                self.list()
            elif type(v) == str:
                self.values = v.split(' ')
                self.list()
            elif type(v) == dict:
                self.dict()

    def list(self):
        for i in self.values:
            if os.path.exists(os.path.join(self.keys, i)):
                try:
                    os.symlink(os.path.join(self.keys, i), i)
                    print('"', i, '"', '执行成功')
                except FileExistsError:
                    print('没有那个文件或文件已经存在')
            else:
                print('Wrong')

    def dict(self):
        pass


def help_():
    pass


def info():
    print('跨越晨昏')


def lists():
    read_yaml('list.yaml')


class Exec:
    def __init__(self, get):
        cleanup_symlinks()
        self.get = get
        if type(get) == dict:
            self.exec_dict()
        elif type(get) == list:
            self.exec_list()
        elif type(get) == str:
            self.get = get.split(' ')
            self.exec_list()
        else:
            print('应该不会发生这种情况,自己查代码吧……')

    def exec_dict(self):
        for k, v in self.get.items():
            if k == 'filing':
                Filing(v)
            elif k == 'working':
                Working(v)
            elif k == 'clean':
                print('清理成功')
            elif k == 'help':
                help_()
            elif k == 'author' or 'crossdark' or 'info':
                info()
            else:
                pass

    def exec_list(self):
        for i in self.get:
            if i == 'clean':
                print('清理成功')
            elif i == 'help':
                help_()
            elif i == 'crossdark' or 'author' or 'info':
                info()


def main():
    try:
        Exec(read_yaml('settings.yaml'))
    except FileNotFoundError:
        make_settings('settings.yaml')


if __name__ == '__main__':
    main()
