def check_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            # 去掉每行两侧的空白字符
            line = line.strip()
            # 按空格拆分行
            elements = line.split()
            # 检查是否至少有两个元素，且第一个元素是否为全英文字母的单词
            word = elements[0]
            if len(elements) > 1:
                sub_words = word.split('-')
                word = "".join(sub_words)
                sub_words = word.split('.')
                word = "".join(sub_words)
            if len(elements) < 2 or not word.isalpha():
                print(f"Line {line_num}: {line}")

# 调用函数并传入文件路径
# file_path = "雅思7600词汇.txt"  # 替换为您的文件路径
file_path = "GRE高频词汇.txt"  # 替换为您的文件路径
check_file_content(file_path)
