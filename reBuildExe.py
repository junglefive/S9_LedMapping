#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyInstaller.__main__ import run
# -F:打包成一个EXE文件
# -w:不带console输出控制台，window窗体格式
# --paths：依赖包路径
# --icon：图标
# --noupx：不用upx压缩
# --clean：清理掉临时文件

if __name__ == '__main__':
    opts = ['-F', '-w', '--paths=C:\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            '--paths=C:\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            '--icon', '110.ico', '--noupx', '--clean',
            'S9LedMapping.py']
    run(opts)
    input()