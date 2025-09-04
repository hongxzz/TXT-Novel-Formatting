#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本清理工具 - Python脚本
BSD 2-Clause License

Copyright (c) 2025, Liu Yunwei

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re
import os
import sys
from tqdm import tqdm

def clean_text_file(input_file_path):
    """
    清理文本文件中的非中英文、数字和标点符号，并删除空行
    
    参数:
        input_file_path (str): 输入文件路径
        
    返回:
        str: 清理后的文件路径
    """
    # 生成输出文件名（添加_cleaned后缀）
    base_name, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base_name}_cleaned{ext}"
    
    # 预编译正则表达式（匹配需要保留的字符）
    # 使用原始字符串并正确转义特殊字符
    pattern = re.compile(
        r'[^\u4e00-\u9fa5a-zA-Z0-9\s,.!?;:，。！？；：\'"“”‘’、~《》〈〉【】〖〗…—\-·]'
    )
    
    try:
        # 第一次遍历：获取文件总行数（用于进度条）
        with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)
        
        # 第二次遍历：处理内容
        with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as in_file, \
             open(output_file_path, 'w', encoding='utf-8', newline='\n') as out_file:
            
            # 使用tqdm创建进度条
            for line in tqdm(in_file, total=total_lines, desc='Processing'):
                # 删除不需要的字符
                cleaned_line = pattern.sub('', line)
                
                # 删除行首尾空白字符并检查是否为空行
                stripped_line = cleaned_line.strip()
                
                if stripped_line:
                    out_file.write(stripped_line + '\n')
        
        return output_file_path
    
    except IOError as e:
        print(f"文件操作错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        sys.exit(1)

def main():
    """
    主函数：处理命令行参数并执行清理操作
    """
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python clean_text.py <input_file>")
        print("说明: 清理文本文件中的非中英文、数字和标点符号，并删除空行")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.isfile(input_path):
        print(f"错误: 文件 '{input_path}' 不存在")
        sys.exit(1)
    
    # 检查文件扩展名
    if not input_path.lower().endswith('.txt'):
        print("警告: 此工具设计用于处理文本文件(.txt)")
    
    # 执行清理操作
    output_path = clean_text_file(input_path)
    print(f"\n清理完成! 文件已保存至: {output_path}")

if __name__ == "__main__":
    main()