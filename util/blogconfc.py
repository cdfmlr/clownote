#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''
@File    : blogconfc.py
@Author  : CDFMLR
@Time    : 2020/07/30 21:49

HEXO BLOG YAML CONFIG CHECKER/COMPLETER

该程序帮助检查并自动补全 hexo 博客文章 YAML 配置。

- API 接口: complete(target_path, *, file_filter=lambda fp: True, verbose=True)
- CLI 接口: $ python3 blogconfc.py [-h] files...
'''

import datetime
import os
import platform
import shutil
import sys
from enum import Enum
from os import path

import yaml


def read_yaml(file_path):
    '''
    read_yaml 从一篇文章中读取 YAML 配置，即在文章开头处两行 `---` 之间的符合 YAML 语法的配置信息。

    参数: 
    
    - file_path: 文章文件路径。
    
    返回:

    - object: yaml.load 返回的 Python object;
    - list  : 原文件中 YAML 配置的起始、结束行（从0开始计数，闭区间）;
    - bool  : 是否存在 YAML 配置。
    '''
    assert os.path.isfile(file_path), f"Target file not exists: {file_path}"

    is_yaml = False
    yaml_content = ''
    yaml_line = []
    lines_cnt = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '---':
                yaml_line.append(lines_cnt)
                if is_yaml or (lines_cnt > 1):
                    break
                is_yaml = not is_yaml
            if is_yaml:
                yaml_content += line.replace('\t', '  ')
            lines_cnt += 1

    return yaml.safe_load(yaml_content), yaml_line, len(yaml_line) == 2


def write_yaml(file_path, yaml_data) -> None:
    '''
    write_yaml 向 file_path 指定的文件开头写入 yaml_data 转化成的 YAML 配置信息，YAML 信息将被前后各一行 `---` 所包裹。

    <em>注意：如果 文章开头已有 YAML 配置，则原有配置**不会**被自动删除或覆盖。本函数仅只是在文件开头添加新的信息！</em>

    输入:

    - file_path: 要写入 YAML 信息的文件路径;
    - yaml_data: 要写入的 YAML 信息对应的 Python 对象，这个对象将被 yaml.dump 序列化为 YAML 文本.

    返回: None
    '''

    yaml_text = yaml.dump(yaml_data, allow_unicode=True)

    wrapper = '---\n'
    yaml_wrapped = wrapper + yaml_text + wrapper

    with open(file_path, "r+") as f:
        file_content = f.read()
        f.seek(0)
        f.write(yaml_wrapped)
        f.write(file_content)


def remove_lines(file_path, lines_range) -> None:
    '''
    remove_lines 从 file_path 指定的文件中将 lines_range 指定的行(闭区间，从0开始计数)删除。

    参数:

    - file_path  : 要删除行的文件路径;
    - lines_range: 要删除的行，闭区间 [start, end]，行数从0开始计.

    返回: None
    '''
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    temp_file = os.path.join(file_dir, f'.{file_name}.tmp')

    shutil.copy(file_path, temp_file)

    with open(temp_file, 'r') as f_in:
        with open(file_path, 'w') as f_out:
            f_out.writelines(line for i, line in enumerate(
                f_in) if i not in range(lines_range[0], lines_range[1]+1))

    os.remove(temp_file)


def get_creation_time(file_path):
    '''
    get_creation_time 获取 file_path 文件的创建时间
    '''
    if platform.platform().find('Darwin') != -1:    # macOS 可以用 birthtime 获取到创建时间
        return os.stat(file_path).st_birthtime
    # 其他系统就用 ctime 吧（Linux 是 change time，inode 里的那种；Windows 据说是 createion time）
    return os.path.getctime(file_path)


def generate_base_conf(file_path) -> dict:
    '''
    generate_base_conf 为 file_path 指定的文件(文章)生成必要的 YAML 配置。

    必要的配置包括：title, date：该函数会从文件的元数据读取信息来设置这两项。

    参数：

    - file_path: 要删除行的文件路径;

    返回：

    - dict: 必要的配置，可用 yaml.dump 成 YAML 的那种
    '''

    # title 取文件名 a.md 中的 a
    title = os.path.basename(file_path)
    title_list = title.split('.')
    if len(title_list) > 1:
        title = ''.join(title_list[:-1])

    # creation_time 取文件创建时间
    creation_time = get_creation_time(file_path)
    date = datetime.datetime.fromtimestamp(creation_time)

    return {'title': title, 'date': date}


def _is_md_file(flie_name: str) -> bool:
    '''
    确定 flie_name 的文件是不是 markdoen 文件
    '''
    return flie_name.lower().endswith('.md')


def md_files_gen(dir, file_filter=lambda fp: True):
    '''
    md_files_gen 返回一个 generator，生成 dir 目录下所有使 file_filter 返回 True 的 `.md` 文件的绝对路径。

    参数:

    - dir        : 遍历起点目录路径;
    - file_filter: 文件过滤器，一个函数，接受文件路径作为参数，返回 True 代表文件应该出现在结果中，返回 False 则忽略这个文件。
    '''
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if _is_md_file(filename):
                file_path = os.path.join(dirpath, filename)
                if file_filter(file_path):
                    yield file_path


def complete_file(file_path, *, verbose=True):
    '''
    complete_file 对 file_path 处的博客文章（`.md` 文件）补全 YAML 配置
    '''
    assert os.path.isfile(file_path) and _is_md_file(file_path)

    conf = generate_base_conf(file_path)
    data, yaml_line, has_yaml = read_yaml(file_path)

    if has_yaml:
        remove_lines(file_path, yaml_line)
    if isinstance(data, dict):
        conf.update(data)

    if conf == data:    # 配置和原本写在文件中的没有改变
        if verbose:
            print(f'配置检查: {file_path} : ok')
    else:
        print(f'配置补全: {file_path} : {data} -> {conf}')

    write_yaml(file_path, conf)


def complete(target_path, *, file_filter=lambda fp: True, verbose=True):
    '''
    complete 补全 target_path 处的博客文章 YAML 配置。

    若 target_path 为博客文章文件（`.md` 文件），且可使 file_filter 返回 True ，则补全该文件的 YAML 配置；
    若 target_path 为目录则补全下所有使 file_filter 返回 True 的 `.md` 文件的 YAML 配置。
    '''
    if os.path.isfile(target_path) and _is_md_file(target_path) and file_filter(target_path):
        complete_file(target_path, verbose=verbose)
    elif os.path.isdir(target_path):
        blogs = md_files_gen(target_path, file_filter)
        for article in blogs:
            complete_file(article, verbose=verbose)


def _print_usage(program_file):
    usage = f'''usage: {program_file} [-h] files...
    补全 files 处的博客文章 YAML 配置。
    -h help: 显示该帮助
    '''
    print(usage)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(sys.argv[0], '参数不足')
        _print_usage(sys.argv[0])
        exit()
    if sys.argv[1] in ['-h', '--help', 'help']:
        _print_usage(sys.argv[0])
        exit()
    for arg in sys.argv[1:]:
        print('检查', arg, '处的博客配置:')
        complete(arg)
        print('配置检查与自动补全完成.')
