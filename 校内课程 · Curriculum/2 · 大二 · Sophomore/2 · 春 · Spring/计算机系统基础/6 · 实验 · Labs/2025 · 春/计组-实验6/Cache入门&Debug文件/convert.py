'''
Author: Wh_Xcjm
Date: 2025-04-09 11:28:02
LastEditor: Wh_Xcjm
LastEditTime: 2025-04-09 11:28:17
FilePath: \Exp6-Cache\convert.py
Description: 

Copyright (c) 2025 by WhXcjm, All Rights Reserved. 
Github: https://github.com/WhXcjm
'''
import csv

def process_row(row):
    # 解析各字段
    reset = int(row[0])
    data_in = int(row[1])
    mem_read = int(row[2])
    mem_write = int(row[3])
    tag = int(row[4])       # 组内块地址
    group_addr = int(row[5]) # 组地址
    block_addr = int(row[6]) # 块内地址

    # 构建32位二进制字符串
    binary_str = (
        f"{reset:01b}"          # 位31
        f"{data_in:017b}"       # 位30-14
        f"{mem_read:01b}"       # 位13
        f"{mem_write:01b}"      # 位12
        f"{tag:06b}"            # 位11-6
        f"{group_addr:02b}"     # 位5-4
        f"{block_addr:02b}"     # 位3-2
        "00"                    # 位1-0 (自动补0)
    )

    # 转换为16进制
    hex_value = f"{int(binary_str, 2):08x}"
    return hex_value

def main():
    with open('data.csv', 'r', encoding='utf8') as csvfile, open('func.hex', 'w') as outfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过标题行
        
        outfile.write("v2.0 raw\n")
        
        for row in reader:
            if row:  # 忽略空行
                hex_value = process_row(row)
                outfile.write(hex_value + "\n")

if __name__ == "__main__":
    main()