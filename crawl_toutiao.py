import requests
import records
import json

db = records.Database("mysql:///....?charset=utf8")
# db.query("""
# create table video_group (
#     id int primary key auto_increment,
#     group_id varchar(50),
#     title varchar(100),
#     data text,
#     comment_count int default 0,
#     like_count int default 0,
#     watch_count int default 0
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# """);

def main():
        url = "http://m.365yg.com/list/"

        querystring = {"tag":"video","ac":"wap","format":"json_raw","cp":"", 'as': "A1A5183CCAA1445"}

        headers = {
            'dnt': "1",
            'accept-encoding': "gzip, deflate, sdch",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            'accept': "*/*",
            'referer': "http://m.365yg.com/?w2atif=1&channel=video&W2atIF=1",
            'cookie': "....",
            'connection': "keep-alive",
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        for item in data['data']:
            group_id = item['group_id']
            title = item['title']
            comment = item.get('comment_count', 0)
            like = item.get('like_count', 0)
            watch = item.get('video_detail_info', {}).get('video_watch_count', 0)
            db.query("""INSERT INTO `video_group` (`group_id`, `title`, `data`, `comment_count`, `like_count`, `watch_count`) VALUES (:group, :title, :data, :comment, :like, :watch); """,
                group=group_id, title=title, data=json.dumps(item), comment=comment, like=like, watch=watch
            )

if __name__ == "__main__":
    main()
