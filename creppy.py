import  pymysql
import requests
import re


def main():
    url = "http://sports.sina.com.cn/nba/"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    resp = requests.get(url, headers=header)
    data = resp.content.decode("utf-8")

    db = pymysql.connect("172.17.0.2", "root", "123456", "mydb", charset='utf8')
    cursor = db.cursor()
    pattern = re.compile("""<a href="(.*)" target="_blank">(.*)</a>""")
    ret = pattern.findall(data)
    lst = []
    insert_stmt = (
        "INSERT INTO NBA(Link,tittle)"
        "VALUES (%s, %s)"
    )
    for i in ret:
            Link = i[0]
            tittle = i[1]
            data = (Link,tittle)
            lst.append(data)
            try:
                cursor.execute(insert_stmt,data)
                db.commit()
            except:
                print
                "insert error"
                db.rollback()
    for i in ret:
            x = (i[0], i[-1])
            "INSERT INTO (Link,tittle)"
            "VALUES (i[0],i[-1])"
    html = """<html>
    <head></head>
    <body>
    <h3>news site</h3>
    <ul>
    """
    for i in lst:
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
