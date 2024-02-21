"""
文件处理
"""
import os
import re
import wget
import ruamel.yaml
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

base_dir = '.'


def ignore(file: str):
    pass


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


def make_symlink(src, dst):
    try:
        os.symlink(src, dst)
    except FileExistsError:  # 文件已经存在
        print(f'{os.path.basename(dst)}链接已经存在')
    else:  # 创建成功
        print(f'{os.path.basename(dst)}链接成功')


def cleanup_symlinks(dir_=base_dir):
    """删除当前目录下的所有符号链接。"""
    if dir_.startswith('.') and dir_ != '.':
        return
    for item in os.listdir(dir_):
        if os.path.islink(os.path.join(dir_, item)):
            os.unlink(os.path.join(dir_, item))
            print(f'{item}清理成功')


class Tree:
    def __init__(self, get):
        print(get)


class Switch:
    """
    处理方法:切换不同文件夹组到目录下
    设置方法:filing:
        <你选中的那组文件夹的父文件夹>(如果设置了多个父文件夹,请确保它们没有名称相同的子文件夹)
    """

    def __init__(self, settings):
        self.base = base_dir  # 根目录
        self.settings = settings  # 传入的设置(可能是str、list、dict)
        self.files = []  # path传入的路径下所有文件
        self.always = []  # always传入的路径下所有文件
        self.temporary = []  # 临时文件(在path中但不在always中)列表
        self.always_files = []  # 永久文件列表(在path中同时也在always中)
        self.file_path = ''  # path传入的路径
        self.always_path = ''  # always传入的路径
        self.output_path = os.path.join(self.base, '.output')  # output传入的路径(存放由files和always_files中的同名文件夹合并而成的目录)
        if type(settings) == str:
            self.settings = settings.split(' ')
            self.list()
        elif type(settings) == list:
            self.list()
        elif type(settings) == dict:
            self.dict()

    def list(self):
        for sets in self.settings:
            if not sets:
                continue
            if os.path.isdir(sets):  # 传入的是目录
                cleanup_symlinks(sets)  # 有什么问题就删了
                for item_name in os.listdir(os.path.abspath(sets)):
                    # 跳过以'.'开头的隐藏文件和目录
                    if item_name.startswith('.'):
                        continue
                    # 创建符号链接
                    make_symlink(os.path.abspath(os.path.join(sets, item_name)),
                                 os.path.abspath(os.path.join(self.base, item_name)))
            elif os.path.isfile(sets):  # 传入的是单个文件
                os.symlink(sets, os.path.join(self.base, sets))
                print('单个文件链接成功')
            else:
                print('请设置path语句')

    def dict(self):
        for k, v in self.settings.items():
            if k == 'path':
                self.files = os.listdir(os.path.abspath(v if type(v) == str else v[0]))
                self.file_path = v
                self.exec_always()
            elif k == 'always':
                self.always = os.listdir(os.path.abspath(v if type(v) == str else v[0]))
                self.always_path = v
            else:
                print('?')

    def make_always(self):
        for file in self.always_files:  #
            cleanup_symlinks(os.path.join(self.always_path, file))
            for i in os.listdir(os.path.join(self.always_path, file)):
                make_symlink(os.path.abspath(os.path.join(self.always_path, file, i)), os.path.join(self.base, file, i))

    def exec_always(self):
        self.always_files = [i for i in self.always if (i in self.files and not i.startswith('.'))]
        self.temporary = [i for i in self.files if i not in self.always_files]
        self.settings = [self.file_path]

        for file in self.files:
            cleanup_symlinks(os.path.join(self.file_path, file))
        self.list()
        cleanup_symlinks(self.always_path)
        self.make_always()


class Working:
    """
    处理方法:将位于不同位置的文件夹集中到当前目录下
    设置方法:working:
        <项目文件夹>
    …………
    """

    def __init__(self, settings):
        self.dir = base_dir
        self.values = settings
        if type(settings) == list:
            self.list()
        elif type(settings) == str:
            self.values = settings.split(' ')
            self.list()
        elif type(settings) == dict:
            self.dict()

    def list(self):
        print(self.values)
        for i in self.values:
            if os.path.exists(os.path.join(self.dir, i)):
                print(os.path.join(i), os.path.join(self.dir, os.path.basename(i)))
                try:
                    os.symlink(os.path.join(i), os.path.join(self.dir, os.path.basename(i)))
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
    wget.download('https://crossdark.com/index.php/2024/02/16/filemachine简介/', os.path.join(base_dir, 'info.txt'))


def lists():
    for i in read_yaml('list.yaml'):
        Exec(i)


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
            if k in ('filing', 'switch'):
                Switch(v)
            elif k == 'working':
                Working(v)
            elif k == 'clean':
                print('清理成功')
            elif k == 'help':
                help_()
            elif k in ('author', 'crossdark', 'info'):
                info()
            elif k == 'dir':
                global base_dir
                base_dir = v
                cleanup_symlinks()
            elif k == 'other':
                Exec(v)
            else:
                print('未知方法')

    def exec_list(self):
        for i in self.get:
            if i == 'clean':
                print('清理成功')
            elif i == 'help':
                help_()
            elif i in ('crossdark', 'author', 'info'):
                info()
            elif i.startswith('dir'):
                global base_dir
                base_dir = i[i.rfind('=') + 1:]
                print(base_dir)
                cleanup_symlinks()
            else:
                print('emm什么鬼')


def main():
    if os.path.exists('settings.yaml'):
        Exec(read_yaml('settings.yaml'))
    elif os.path.exists('.FileMachine.yaml'):
        Exec(read_yaml('.FileMachine.yaml'))
    else:
        make_settings('settings.yaml')


if __name__ == '__main__':
    main()
