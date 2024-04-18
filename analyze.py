'''
Author: LIKE_A_STAR
Date: 2024-03-10 18:15:03
LastEditors: LIKE_A_STAR
LastEditTime: 2024-03-16 22:23:06
Description: 
FilePath: \vscode program\Python file\bilibili\analyze.py
'''
import jieba
import csv
import yaml

def AnalyzeWrods(csv_path):
    txt = ""
    csv_reader = csv.reader(open(csv_path))
    for row in csv_reader:
        txt += row[0]
    words = jieba.lcut(txt)

    stopwords = [line.strip() for line in open("./pkg/cn_stopwords.txt", encoding="utf-8").readlines()]
    counts = {}
    for word in words:
        if word not in stopwords:
            if len(word) != 1:
                counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)

    for i in range(30):
        word, count = items[i]
        print ("{:<10}{:>7}".format(word, count))
    return items[:30]

# 将其中一行复制到txt中
def AnalyzeTxt(path):
    txt = ""
    txt_reader = open(path, "r", encoding='utf-8')
    for row in txt_reader:
        txt += row
    words = jieba.lcut(txt)

    stopwords = [line.strip() for line in open("./pkg/cn_stopwords.txt", encoding="utf-8").readlines()]
    counts = {}
    for word in words:
        if word not in stopwords:
            if len(word) != 1:
                counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)

    for i in range(30):
        word, count = items[i]
        print ("{:<10}{:>7}".format(word, count))
    return items[:30]

def WriteSummary(lists, txt_path):
    data = {}
    for i in lists:
        for j in i:
            data[j[0]] = data.get(j[0], 0) + j[1]

    items = list(data.items())
    items.sort(key=lambda x:x[1], reverse=True)
    print(len(items))
    # for i in range(len(items)):
    #     print(i)
    #     if items[i][1] < 100:
    #         items = items[:i]
    #         break
    fp = open(txt_path, "a+")
    for word in items:
        fp.write(word[0])
        fp.write("\n")
    fp.close()

if __name__ == '__main__':
    # with open('config.yaml', 'r', encoding="utf-8") as f:
    #     config = yaml.safe_load(f)
    #     f.close()
    # lists = []
    # for oid in config["oid"]:
    #     lists.append(AnalyzeWrods(f'./src/{oid}.csv'))
    #     print("\n")

    # WriteSummary(lists, "./src/sum.txt")

    # Cloud("./src/1450893212.csv", "comment.png")

    lists = []
    lists.append(AnalyzeTxt('./src/aaa.txt'))
    WriteSummary(lists, "./src/sum2.txt")
