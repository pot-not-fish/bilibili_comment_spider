import requests
import yaml
import json
import time
import urllib
import time
import hashlib
import csv

class Comment():
    def __init__(self):
        with open('config.yaml', 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f)
            f.close()
        self.config = config

        headers = {
                "Accept":             config["headers"]["Accept"],
                "Accept-Encoding":    config["headers"]["Accept-Encoding"],
                "Accept-Language":    config["headers"]["Accept-Language"],
                "Cookie":             config["headers"]["Cookie"],
                "Origin":             config["headers"]["Origin"],
                "Referer":            config["headers"]["Referer"],
                "Sec-Fetch-Dest":     config["headers"]["Sec-Fetch-Dest"],
                "Sec-Fetch-Mode":     config["headers"]["Sec-Fetch-Mode"],
                "Sec-Fetch-Site":     config["headers"]["Sec-Fetch-Site"],
                "User-Agent":         config["headers"]["User-Agent"],
                "authority":          config["headers"]["authority"],
                "Sec-Ch-Ua":          config["headers"]["Sec-Ch-Ua"],
                "Sec-Ch-Ua-Mobile":   config["headers"]["Sec-Ch-Ua-Mobile"],
                "Sec-Ch-Ua-Platform": config["headers"]["Sec-Ch-Ua-Platform"]
        }
        self.headers = headers

    def GetAllVideosComments(self):
        for oid in self.config["oid"]:
            self.GetAllComments(oid)

    def GetAllComments(self, oid):
        headers = ['content', 'mid', 'like']
        with open('./src/{oid}.csv'.format(oid=oid),'a+', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(headers)
            fp.close()
            
        pagination_str = """{"offset":""}"""
        isEnd, nextOffset = self.GetComments(oid, pagination_str, "&seek_rpid=")
        while not isEnd:
            isEnd, nextOffset = self.GetComments(oid, nextOffset, "")
            if isEnd:
                break
            data = json.loads(nextOffset)
            session_id = data["session_id"]
            a = """{"offset":"{\\"type\\":1,\\"direction\\":1,\\"session_id\\":\\\""""
            b = """\\",\\"data\\":{}}"}"""
            nextOffset = a + session_id + b

    def GetWrid(self, oid, pagination_str, seek_rpid):
        url_text = urllib.parse.quote(pagination_str)
        timestamp = int(time.time())
        load = "mode=3&oid={oid}&pagination_str={url_text}&plat=1{seek_rpid}&type=1&web_location=1315875&wts={timestamp}ea1db124af3c7062474693fa704f4ff8".format(oid = oid, url_text = url_text, seek_rpid = seek_rpid, timestamp = timestamp)
        m = hashlib.md5()
        m.update(load.encode())
        return m.hexdigest(), timestamp

    def GetComments(self, oid, pagination_str, seek_rpid):
        w_rid, wts = self.GetWrid(oid, pagination_str, seek_rpid)

        payload = {
            "oid":            oid,
            "type":           self.config["payload"]["type"],
            "mode":           self.config["payload"]["mode"],
            "plat":           self.config["payload"]["plat"],
            "web_location":   self.config["payload"]["web_location"],
            "w_rid":          w_rid,
            "wts":            wts,
            "pagination_str": pagination_str
        }

        if seek_rpid != "":
            payload["seek_rpid"] = ""

        resp = requests.get("https://api.bilibili.com/x/v2/reply/wbi/main", params = payload, headers = self.headers)

        print(resp.url)

        data = json.loads(resp.text)
        columns = []
        if seek_rpid != "":
            return data["data"]["cursor"]["is_end"], data["data"]["cursor"]["pagination_reply"]["next_offset"]
        for i in data["data"]["replies"]:
            columns.append((i["content"]["message"], i["mid"], i["like"]))

        with open('./src/{oid}.csv'.format(oid=oid),'a+', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(columns)
            print(wts, "写入成功")
            fp.close()

        time.sleep(2)

        if data["data"]["cursor"]["is_end"]  == True:
            return True, ""
        return data["data"]["cursor"]["is_end"], data["data"]["cursor"]["pagination_reply"]["next_offset"]


if __name__ == '__main__':
    c = Comment()
    c.GetAllVideosComments()