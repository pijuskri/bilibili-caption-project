from fuzzychinese import FuzzyChineseMatch
a = ["凉拌鱼皮亮晶晶酸爽入口有韧性", "第一次尝炸鱼饼香香软软味不腥"]
b = ["第一次尝炸鱼饼香香软软味不醒"]
fcm = FuzzyChineseMatch(ngram_range=(5, 5), analyzer='stroke')
fcm.fit(a)
top2_similar = fcm.transform(b, n=2)
print(max(fcm.get_similarity_score()[0]))