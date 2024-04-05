import re
import pandas as pd


def remove_text(text, pattern):
    return re.sub(pattern, '', text)


def parse_txt(filename, start_word):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()

    # 删除特定文本
    data = remove_text(data, r'本文档由陈琦和周书林共同制作完成。未经作者授权，严禁将此文档用于商业用途。')
    data = remove_text(data,r'Made By Jason & Franklin. This Document Is Strictly Prohibited For Commercial Purposes Without Authorization.')

    entries = re.split(r'\n{3,}', data.strip())

    dictionary_list = []
    found_begin = False

    for entry in entries:
        word_match = re.match(r'^(\w+)\s+\[([^]]+)]', entry)
        if word_match:
            word = word_match.group(1)

            if start_word in word or found_begin:
                found_begin = True
            else:
                continue

            definitions = re.findall(r'【考法(?:\s+\d+)?】([^【]+)', entry)
            examples = re.findall(r'【例】([^【]+)', entry)

            clean_definitions = [s.strip().replace('\n', '') for s in definitions]

            clean_examples = []
            for s in examples:
                if '‖' in s:
                    for e in s.split('‖'):
                        clean_examples.append(
                            re.sub(r'([a-zA-Z])\s*([\u4e00-\u9fff])', r'\1  \2',
                                   re.sub(r'\.', '.  ', e.strip().replace('\n', '')))
                        )
                else:
                    clean_examples.append(
                        re.sub(r'([a-zA-Z])\s*([\u4e00-\u9fff])', r'\1  \2',
                               re.sub(r'\.', '.  ', s.strip().replace('\n', '')))
                    )

            dictionary_entry = {
                'word': word,
                'definitions': clean_definitions,
                'examples': clean_examples
            }

            dictionary_list.append(dictionary_entry)

    return dictionary_list


def get_excel(filename, start_word, num):
    dictionary_list = parse_txt(filename, start_word)
    num_entries = len(dictionary_list)
    entries_per_file = num_entries // num

    for i in range(num):
        df = pd.DataFrame(columns=['单词', '含义（可不填）', '例句（可不填）', '标签（可不填，多个标签请用英文逗号分隔）'])
        rows = []
        start_index = i * entries_per_file
        end_index = start_index + entries_per_file if i < num-1 else num_entries  # 最后一份可能会多一些
        for item in dictionary_list[start_index:end_index]:
            word = item['word']
            definitions = '\n'.join(item['definitions'])
            examples = '\n'.join(item['examples'])
            rows.append({'单词': word, '含义（可不填）': definitions, '例句（可不填）': examples,
                        '标签（可不填，多个标签请用英文逗号分隔）': 'GRE'})
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        df.to_excel(f'result/生词本导入模版_{i+1}.xlsx', index=False)


if __name__ == '__main__':
    filename = 'words.txt'
    start_word = 'impugn'
    num = 12
    get_excel(filename, start_word, num)
