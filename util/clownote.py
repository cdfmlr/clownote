#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''
@File    : clownote.py
@Author  : CDFMLR
@Time    : 2020/07/31 15:30
@Update  : 2020/08/19 10:33

clownote Hexo 博客实用工具。

该程序将 clownote 使用实践中高复用的 hexo, git 以及 blogconfc.py 调用流程封装在一起，以简化工作流程。

目前提供如下接口:

- check: 调用 blogconfc.py 检查并自动补全博客文章配置，并自动开启 hexo serve 预览改变;
- push:  调用 git 提交更新，并推送至远程仓库, 在提交前会自动执行一次 check;

⚠️ 注意：在该文件中设置有一个全局常量 `CLOWNOTE_PATH`，需将该其值设为 clownote Hexo 博客的根目录绝对路径。
'''

import argparse
import os
import subprocess
from functools import partial
from os import path

from blogconfc import complete


# CLOWNOTE_PATH 为 clownote Hexo 博客的根目录绝对路径
CLOWNOTE_PATH = '/Users/c/clownote'


# run 是 subprocess.run 的偏函数，固定了常用配置，简化后续代码中的调用
run = partial(subprocess.run, shell=False, stdout=subprocess.PIPE,
              stderr=subprocess.PIPE, encoding="utf-8")


def check_changed(**kwargs):
    '''
    检查、补全配置，调用 hexo serve 预览站点。
    返回仓库中所有改变的文件路径（包括一切文章与非文章文件）。

    kwargs:

    - preview_serve: bool: 是否调用 hexo serve 预览站点 (default: True);
    - verbose: bool: 显示更详细的执行信息;
    '''
    preview_serve = kwargs.get('preview_serve', True)
    verbose = kwargs.get('verbose', False)

    os.chdir(CLOWNOTE_PATH)

    # 添加“尚未暂存以备提交的变更”
    run(['git', 'add', '-N', '.'])

    # 获取改变了的文件
    res = run(['git', 'diff', '--name-only'])
    changed = res.stdout.strip().split('\n')

    # 检查、补全配置
    for article in changed:
        complete(article, verbose=verbose)

    if not preview_serve:
        return changed

    print('正在启动 hexo serve 预览...')
    try:
        # stdout=None: 不捕获输出，即放任输出显示到 stdout
        run(['hexo', 'serve'], stdout=None)
    except KeyboardInterrupt:
        print('KeyboardInterrupt: Hexo serve is stopped.')

    return changed


def push(**kwargs):
    '''
    调用 check(verbose=False) 检查一次配置，然后 git 提交所有文件更改。

    kwargs:

    - message: str : git commit 提交的 message 信息；
    - verbose: bool: 显示更详细的执行信息;
    '''
    message = kwargs.get('message', '')
    if len(message) != 0:
        message += '\n\n'
    verbose = kwargs.get('verbose', False)

    os.chdir(CLOWNOTE_PATH)

    # 检查有更改的文件的配置，不预览
    changed = check_changed(preview_serve=False, verbose=verbose)
    if len(changed) == 0:
        changed.append('None')
    names = map(lambda f: os.path.basename(f).rstrip('.md'), changed)
    commit_msg = message + \
        'changed files: ' + ', '.join(names) + \
        '\n\n[Automatically， clownote]'

    # Git 提交
    # 如果 verbose，就要把提交过程的输出信息显示到屏幕
    n_cmd = partial(run, stdout=None, stderr=None) if verbose else run

    n_cmd(['git', 'add', '.'])
    n_cmd(['git', 'commit', '-m', commit_msg])
    n_cmd(['git', 'push'])


def main():
    description = 'Clownote Hexo 博客实用工具'
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(
        title='subcommands', description='valid subcommands')

    # 子命令 check
    description_check = '调用 blogconfc.py 检查并自动补全博客文章配置，启动 hexo serve 预览站点'
    parser_check = subparsers.add_parser(
        'check', aliases=['c'], help=description_check, description=description_check)
    parser_check.set_defaults(func=check_changed)
    parser_check.add_argument('-n', '--no-preview',
                              '--no-serve', help='不调用 hexo serve 预览', action="store_true")

    # 子命令 push
    description_push = '调用 git 提交更新，并推送至远程仓库, 在提交前会自动执行一次 check'
    parser_push = subparsers.add_parser(
        'push', aliases=['p'], help=description_push, description=description_push)
    parser_push.set_defaults(func=push)
    parser_push.add_argument('-m', '--message',
                             help='Use the given MESSAGE as the commit message.', action='store')

    # check、push 通用的 verbose 选项
    for p in [parser_check, parser_push]:
        p.add_argument("-v", "--verbose",
                       help="increase output verbosity", action="store_true")

    # 解析命令行参数
    args = parser.parse_args()

    # 执行相应的函数，或打印帮助
    if not hasattr(args, 'func'):
        parser.print_help()
    elif args.func is check_changed:
        preview = not args.no_preview if hasattr(
            args, 'no_preview') else False
        check_changed(preview_serve=preview, verbose=args.verbose)
    elif args.func is push:
        message = args.message if hasattr(args, 'message') else ''
        push(message=message, verbose=args.verbose)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
