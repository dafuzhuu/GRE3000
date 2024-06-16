import re
import time
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font


def remove_text(text, pattern):
    return re.sub(pattern, '', text)


def parse_txt(filename, start_word):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()

    entries = re.split(r'\n{2,}', data.strip())

    dictionary_list = []
    found_begin = False

    for entry in entries:
        word_match = re.match(r"Q:(\w+(?:-\w+)*)\s*\[", entry)
        if word_match:
            word = word_match.group(1)

            if start_word in word or found_begin:
                found_begin = True
            else:
                continue

            definitions = re.findall(r'♠考法\d+\s+(.*?)\n', entry)
            examples = re.findall(r'♣例\s+(.*?)\n', entry)

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
    word_dictionary = parse_txt(filename, start_word)
    dictionary_list = parse_txt(filename, start_word)
    num_entries = len(dictionary_list)
    entries_per_file = num_entries // num

    for i in range(num):
        df = pd.DataFrame(columns=['单词', '含义（可不填）', '例句（可不填）', '标签（可不填，多个标签请用英文逗号分隔）'])
        rows = []
        start_index = i * entries_per_file
        end_index = start_index + entries_per_file if i < num - 1 else num_entries  # 最后一份可能会多一些
        for item in dictionary_list[start_index:end_index]:
            word = item['word']
            definitions = '\n'.join(item['definitions'])
            examples = '\n'.join(item['examples'])
            rows.append({'单词': word, '含义（可不填）': definitions, '例句（可不填）': examples,
                         '标签（可不填，多个标签请用英文逗号分隔）': 'GRE'})
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        df.to_excel(f'result/生词本导入模版_{i + 1}.xlsx', index=False)


def search_console(filename, start_word):
    word_dictionary = parse_txt(filename, start_word)

    def query_word(event=None):
        word = word_entry.get().strip()
        word_text.config(text=word)
        definitions, examples = None, None
        for entry in word_dictionary:
            if entry['word'] == word:
                definitions = entry['definitions']
                examples = entry['examples']
                break

        if definitions and examples:
            definition_text.config(text="\n".join(definitions))
            example_text.config(text='♠ ' + "\n♠ ".join(examples))
        elif definitions:
            definition_text.config(text="\n".join(definitions))
            example_text.config(text='')
        else:
            definition_text.config(text="错误")
            example_text.config(text="未找到该单词的定义和例句")

        word_entry.delete(0, tk.END)

    # 创建主窗口
    root = tk.Tk()
    root.title("GRE单词查询")

    # 字体大小
    my_font = tk.font.Font(family='ComicSansMS', size=18)

    # 创建输入框和按钮
    label = tk.Label(root, text="请输入要查询的单词：", font=my_font)
    label.pack(pady=5)

    word_entry = tk.Entry(root, width=30, font=my_font)
    word_entry.pack(pady=5)
    word_entry.bind("<Return>", query_word)  # 绑定回车键触发查询

    button = tk.Button(root, text="查询", command=query_word, font=my_font)
    button.pack(pady=5)

    # 创建文本框显示单词、定义和例句
    word_text = tk.Label(root, wraplength=600, justify=tk.LEFT, font=tk.font.Font(family='ComicSansMS', size=20))
    word_text.pack(pady=2)

    definition_label = tk.Label(root, text="定义：", font=my_font)
    definition_label.pack(pady=5)

    definition_text = tk.Label(root, wraplength=600, justify=tk.LEFT, font=my_font)
    definition_text.pack(pady=5)

    example_label = tk.Label(root, text="例句：", font=my_font)
    example_label.pack(pady=5)

    example_text = tk.Label(root, wraplength=700, justify=tk.LEFT, font=my_font)
    example_text.pack(pady=5)

    root.geometry("800x600+400+50")
    root.mainloop()


# 从impugn开始录的，前面是手打，释义和例句不全
# 不要把impugn前的全录进去，而是把重合的部分录进去（因为有些很熟了）
def overlap_words(filename, start_word):
    # filename = 'words_github.txt'
    # start_word = 'impugn'
    txt = parse_txt(filename, start_word)
    txt_keys = [txt[i]['word'] for i in range(len(txt))]
    # get_excel(filename, start_word, num)

    shengci = pd.read_excel("生词本.xlsx")
    # 生词本中所有词
    all_words = shengci["单词"].values.tolist()

    # 生词本内除了impugn以后的
    remove_from_impugn = list(set(all_words) - set(txt_keys))
    all_3000_words_txt = parse_txt(filename, "abandon")
    missing_words = [all_3000_words_txt[i]['word'] for i in range(len(all_3000_words_txt))]
    # abandon ~ impugn
    missing_words = list(set(missing_words) - set(txt_keys))

    overlap = list(set(remove_from_impugn) & set(missing_words))

    # 要你命3000中所有词
    get_excel(filename, "abandon", 1)
    all_3000_words = pd.read_excel("./result/生词本导入模版_1.xlsx")
    selected_words = all_3000_words[all_3000_words["单词"].isin(overlap)]
    # selected_words.to_excel("./result/补.xlsx", index=False)
    return selected_words


if __name__ == '__main__':

    filename = 'words_github.txt'
    start_word = 'abandon'
    num = 1
    txt = parse_txt(filename, start_word)
    txt_keys = [txt[i]['word'] for i in range(len(txt))]
    # get_excel(filename, start_word, num)

    # 单词搜索
    search_console(filename, start_word)
