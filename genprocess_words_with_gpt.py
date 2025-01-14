import openai
import json
import time

# 设置 OpenAI API 密钥
openai.api_key = "1111"

# 输入和输出文件路径
# input_file_path = "雅思7600词汇.txt"
# output_file_path = "雅思7600词汇.json"
input_file_path = "GRE高频词汇.txt"
output_file_path = "GRE高频词汇.json"

def get_phonetic_and_sentence(word):
    """
    调用 ChatGPT API 获取单词的音标和例句
    """
    result = None
    phonetic = None
    sentence = None
    try:
        # 构造提示语
        prompt = f'请为以下单词生成音标和例句：\n单词：{word}\n要求：\n1. 提供标准音标（使用国际音标IPA）。\n2. 提供一个例句，例句中应尽量使用日常口语化的词汇。\n3.返回数据的格式必须为："音标: [音标内容];例句: <例句内容>"'
        
        # 调用 ChatGPT API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的语言学家。"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        
        # 从 API 响应中提取结果
        result = response.choices[0].message.content
        # result = response['choices'][0]['message']['content']
        phonetic = result.split("音标: ")[1].split(";")[0].strip()
        phonetic_0 = phonetic.strip("[]").strip()
        phonetic_1 = phonetic.strip("//").strip()
        if len(phonetic_0) > 0:
            phonetic = phonetic_0
        elif len(phonetic_1) > 0:
            phonetic = phonetic_1
        phonetic = f'/{phonetic}/'
        sentence = result.split("例句: ")[1].strip("<>").strip()
        sentence = sentence.split(">")[0].strip()
        return phonetic, sentence
    except Exception as e:
        print(f"Error generating data for word '{word}'; result - '{result}'; execption: {e}")
        time.sleep(0.5)
        return None, None

def process_words(file_path):
    """
    读取单词文件并生成 JSON 数据
    """
    words_data = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(" ")
            if len(parts) < 2:
                continue
            word = parts[0]
            meaning = "".join(parts[1:])
            
            # 调用函数获取音标和例句
            retry_count = 0
            max_retries = 1000
            while retry_count < max_retries:
                phonetic, sentence = get_phonetic_and_sentence(word)
                if phonetic and sentence:
                    break
                retry_count += 1
            if retry_count == max_retries:
                print(f"Failed to generate data for word '{word}' after {max_retries} retries. Skipping...")
                phonetic, sentence = "", ""
                # continue
            if phonetic and sentence:
                word_entry = {
                    "word": word,
                    "phonetic": phonetic,
                    "meaning": meaning,
                    "example_sentence": sentence,
                }
                words_data.append(word_entry)
    
    return words_data

def save_to_json(data, file_path):
    """
    将数据保存到 JSON 文件
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    print("Processing words from the file...")
    words_data = process_words(input_file_path)
    print(f"Processed {len(words_data)} words. Saving to JSON...")
    save_to_json(words_data, output_file_path)
    print(f"Data saved to {output_file_path}")

if __name__ == "__main__":
    main()
