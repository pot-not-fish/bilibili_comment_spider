from wordcloud import WordCloud
import matplotlib.pyplot as plt

def Cloud(txt_path, cloud_path):
    txt = open(txt_path, "r", encoding='utf-8').read()

    wordcloud = WordCloud(
        background_color="white", 
        width=1000, 
        height=860,
        font_path='./pkg/msyh.ttc' # 没有指定样式就无法生成相应的词云图
    ).generate(txt)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    wordcloud.to_file(cloud_path)

if __name__ == '__main__':
    Cloud('./src/filter2.txt', './src/cloud2.png')