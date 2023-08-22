#!/bin/bash

# 遍历当前目录下所有以log_开头的文件夹
for dir in test_*; do
    # 检查该目录是否存在
    if [ -d "$dir" ]; then
        # 遍历该目录下的所有.log文件
        for file in "$dir"/*.txt; do
            # 检查该文件是否存在
            if [ -f "$file" ]; then
                # 使用 > 将文件内容重定向到自身，从而清空文件内容
                > "$file"
            fi
        done
    fi
done