import  pymysql
import requests
import re

def main():
    url1 = "http://sports.sina.com.cn/nba/"
    url2 = "http://sports.ifeng.com/nba/"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    resp = requests.get(url1, headers=header)
    data1 = resp.content.decode("utf-8")
    resp = requests.get(url2, headers=header)
    data2 = resp.content.decode("utf-8")
    print (data2)
    db = pymysql.connect("172.17.0.2", "root", "123456", "mydb", charset='utf8')
    cursor = db.cursor()
    pattern1 = re.compile("""<a href="(.*)" target="_blank">(.*)</a>""")
    pattern2 = re.compile("""<a target="_blank" tittle=(.*) href=(.*)</a>""")
    ret1 = pattern1.findall(data1)
    ret2 = pattern2.findall(data2)
    print (ret2)
    lst1 = []
    lst2 = []
    insert_stmt = (
        "INSERT INTO NBA(Link,tittle)"
        "VALUES (%s, %s)"
    )
    for i in ret1:
            Link = i[0]
            tittle = i[1]
            data = (Link,tittle)
            lst1.append(data1)
            try:
                cursor.execute(insert_stmt,data)
                db.commit()
            except:
                print
                "insert error"
                db.rollback()
    for i in ret2:
            Link = i[0]
            tittle = i[1]
            data = (Link,tittle)
            lst2.append(data2)
            try:
                cursor.execute(insert_stmt,data)
                db.commit()
            except:
                print
                "insert error"
                db.rollback()
    for i in ret1:
            x = (i[0], i[-1])
            "INSERT INTO (Link,tittle)"
            "VALUES (i[0],i[-1])"
    html = """<html>
    <head></head>
    <body>
    <h3>news site</h3>
    <ul>
    """
    for i in lst1:
        html += """<li><a href="""
        html += i[0]
        html += """">"""
        html += i[1]
        html += """</a></li>"""
    html += """</ul></body></html>"""

    with open("01.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
