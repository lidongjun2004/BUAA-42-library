import heapq
import os
import struct
from collections import Counter
from typing import Dict, List, Tuple, Optional

class HuffmanNode:
    """霍夫曼树节点类"""
    def __init__(self, char: Optional[str], freq: int):
        self.char = char  # 字符，内部节点为None
        self.freq = freq  # 频率
        self.left: Optional[HuffmanNode] = None
        self.right: Optional[HuffmanNode] = None
    
    # 用于堆排序的比较方法
    def __lt__(self, other: 'HuffmanNode') -> bool:
        return self.freq < other.freq


class HuffmanCoding:
    """霍夫曼编码压缩类"""
    
    def __init__(self):
        self.codes: Dict[str, str] = {}  # 字符->编码映射
        self.reverse_mapping: Dict[str, str] = {}  # 编码->字符映射
    
    def _frequency_analysis(self, text: str) -> Dict[str, int]:
        """统计字符频率"""
        return Counter(text)
    
    def _build_huffman_tree(self, frequencies: Dict[str, int]) -> Optional[HuffmanNode]:
        """构建霍夫曼树"""
        # 创建叶节点优先队列
        heap = []
        for char, freq in frequencies.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        
        # 合并节点直到只剩一个根节点
        while len(heap) > 1:
            # 取出频率最小的两个节点
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # 创建新内部节点，频率为两子节点之和
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def _generate_codes_helper(self, root: HuffmanNode, current_code: str):
        """递归生成霍夫曼编码"""
        if root is None:
            return
        
        # 叶节点：存储字符的编码
        if root.char is not None:
            if current_code == "":
                current_code = "0"  # 处理只有一个字符的特殊情况
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        
        # 遍历左子树，编码加'0'
        self._generate_codes_helper(root.left, current_code + "0")
        # 遍历右子树，编码加'1'
        self._generate_codes_helper(root.right, current_code + "1")
    
    def _generate_codes(self, root: HuffmanNode):
        """生成霍夫曼编码表"""
        self.codes = {}
        self.reverse_mapping = {}
        self._generate_codes_helper(root, "")
    
    def _encode_text(self, text: str) -> str:
        """将文本编码为二进制字符串"""
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text
    
    def _pad_encoded_text(self, encoded_text: str) -> str:
        """填充编码文本使其长度为8的倍数"""
        extra_padding = 8 - (len(encoded_text) % 8)
        
        # 添加填充位
        for _ in range(extra_padding):
            encoded_text += "0"
        
        # 添加填充信息（前8位表示填充位数）
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        
        return encoded_text
    
    def _get_byte_array(self, padded_encoded_text: str) -> bytearray:
        """将二进制字符串转换为字节数组"""
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("编码文本长度必须是8的倍数")
        
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte_segment = padded_encoded_text[i:i+8]
            b.append(int(byte_segment, 2))
        
        return b
    
    def compress_file(self, input_path: str, output_path: str):
        """压缩文件主函数"""
        # 读取原始文件
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        if not text:
            print("文件为空")
            return
        
        print(f"原始文件大小: {len(text)} 字符")
        
        # 1. 频率分析
        frequencies = self._frequency_analysis(text)
        print(f"不同字符数: {len(frequencies)}")
        
        # 2. 构建霍夫曼树
        root = self._build_huffman_tree(frequencies)
        
        # 3. 生成编码表
        self._generate_codes(root)
        
        # 4. 编码文本
        encoded_text = self._encode_text(text)
        
        # 5. 填充和转换
        padded_encoded_text = self._pad_encoded_text(encoded_text)
        byte_array = self._get_byte_array(padded_encoded_text)
        
        # 6. 写入压缩文件
        with open(output_path, 'wb') as output:
            # 写入文件头：编码表信息
            # 格式：字符数(2字节) + 每个字符(字符(1字节), 编码长度(1字节), 编码)
            output.write(struct.pack('H', len(self.codes)))  # 字符数
            
            # 写入编码表
            for char, code in self.codes.items():
                char_byte = char.encode('utf-8')[0] if len(char) == 1 else 0
                code_length = len(code)
                # 将编码转换为字节
                code_bytes = self._code_to_bytes(code)
                output.write(struct.pack('B', char_byte))
                output.write(struct.pack('B', code_length))
                output.write(code_bytes)
            
            # 写入压缩数据大小和压缩数据
            output.write(struct.pack('I', len(byte_array)))  # 数据长度
            output.write(byte_array)
        
        # 计算压缩率
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = compressed_size / original_size
        
        print(f"压缩完成!")
        print(f"原始文件大小: {original_size} 字节")
        print(f"压缩文件大小: {compressed_size} 字节")
        print(f"压缩率: {compression_ratio:.2%}")
        
        return compression_ratio
    
    def _code_to_bytes(self, code: str) -> bytes:
        """将二进制编码字符串转换为字节"""
        # 将二进制字符串补足到8的倍数
        padding = 8 - (len(code) % 8)
        if padding != 8:
            code = code + '0' * padding
        
        # 转换为字节
        byte_array = bytearray()
        for i in range(0, len(code), 8):
            byte_segment = code[i:i+8]
            byte_array.append(int(byte_segment, 2))
        
        return bytes(byte_array)


def main():
    """主函数"""
    # 配置参数
    input_file = "origin.txt"  # 原始文件
    output_file = "text.huff"  # 压缩文件
    
    # 创建霍夫曼编码器并压缩文件
    huffman = HuffmanCoding()
    compression_ratio = huffman.compress_file(input_file, output_file)
    
    return compression_ratio


if __name__ == "__main__":
    main()