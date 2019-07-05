import  pymysql
import requests
import re

def main():
    url1 = "http://sports.sina.com.cn/nba/"
    url2 = "https://news.baidu.com/sports"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    resp = requests.get(url1, headers=header)
    data1 = resp.content.decode("utf-8")
    resp = requests.get(url2, headers=header)
    data2 = resp.content.decode("utf-8")
    db = pymysql.connect("172.17.0.2", "root", "123456", "mydb", charset='utf8')
    cursor = db.cursor()
    pattern1 = re.compile("""<a href="(.*)" target="_blank">(.*)</a>""")
    pattern2 = re.compile("""<a href="(.*)" mon="(.*)" target="_blank">(.*)</a>""")
    ret1 = pattern1.findall(data1)
    ret2 = pattern2.findall(data2)
    lst1 = []
    lst2 = []
    insert_stmt = (
        "INSERT INTO SPORTNEWS(Link,tittle)"
        "VALUES (%s, %s)"
    )
    for i in ret1:
            Link = i[0]
            tittle = i[1]
            data1 = (Link,tittle)
            lst1.append(data1)
            try:
                cursor.execute(insert_stmt,data1)
                db.commit()
            except:
                print
                "insert error"
                db.rollback()
    for i in ret2:
            Link = i[0]
            tittle = i[-1]
            data2 = (Link,tittle)
            lst2.append(data2)
            try:
                cursor.execute(insert_stmt,data2)
                db.commit()
            except:
                print
                "insert error"
                db.rollback()
    for i in ret1:
            x = (i[0], i[-1])
            "INSERT INTO (Link,tittle)"
            "VALUES (i[0],i[-1])"
    for i in ret2:
            x = (i[0], i[-1])
            "INSERT INTO (Link,tittle)"
            "VALUES (i[0],i[-1])"
    html1 = """<html>
    <head></head>
    <body>   
    <h3>sport news site</h3>
    <h4>from sina </h4>
    <ul>
    """
    for i in lst1:
        html1 += """<li><a href="""
        html1 += i[0]
        html1 += """">"""
        html1 += i[1]
        html1 += """</a></li>"""
    html1 += """</ul></body></html>"""
    html2 = """<html>
        <head></head>
        <body>
        <h4>from baidu </h4>
        <ul>
        """
    for i in lst2:
        html2 += """<li><a href="""
        html2 += i[0]
        html2 += """">"""
        html2 += i[-1]
        html2 += """</a></li>"""
    html2 += """</ul></body></html>"""

    with open("01.html", "w", encoding="utf-8") as f:
        f.write(html1)
        f.write(html2)

if __name__ == "__main__":
    main()
