
import requests
import json
import urllib.parse

def loadbuilding():
    with open("building.json","rb")as f:
        js=f.read()
        js=json.loads(js)
        buildings=js["query_elec_building"]["buildingtab"]
        return buildings

def askInfo():
    print("校园卡帐号(6位左右)")
    account = input()
    print("选择你的building")
    buildings = loadbuilding()
    for index, item in enumerate(buildings):
        print(f"[{index}] {item['building']}")
    buildingId = int(input())
    print(f"选择了 {buildingId} {buildings[buildingId]}")
    print("输入房间")
    room = input()
    return account,buildings[buildingId],room

if __name__ == '__main__':
    try:
        with open("memory.json","rb")as f:
            js=json.loads(f.read())
            account=js["account"]
            building=js["building"]
            room=js["room"]
        print(f"读取到历史查询room {account} {building} {room}")
        print("重新输入信息请删除 memory.json")
    except Exception as e:
        print(e)
        account,building,room=askInfo()
        with open("memory.json",'w',encoding='utf=8')as f:
            js={
                "account":account,
                "building":building,
                "room":room,
            }
            json.dump(js,f,ensure_ascii=False)
            print("记住辣! 重新输入信息请删除 memory.json")
    session=requests.session()
    # Content-Type是必要的
    header={
        "User-Agent":"""Mozilla/5.0 (Linux; Android 10; SM-G9600 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36""",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    }
    data=""
    with open("post.json","rb")as f:
        js=f.read()
        js=json.loads(js)

        js["query_elec_roominfo"]["account"]=account
        js["query_elec_roominfo"]["room"]["roomid"]=room
        js["query_elec_roominfo"]["room"]["room"]=room
        js["query_elec_roominfo"]["building"]=building

        js=json.dumps(js,ensure_ascii=False)
        print(js)

        js=urllib.parse.quote(js)
        data+=js


    data="jsondata="+data+"&funname=synjones.onecard.query.elec.roominfo&json=true"
    print(data)
    res=session.post(url="http://10.100.1.24:8988/web/Common/Tsm.html",headers=header,data=data)
    print("res!!!!!!!!!!!!!!!")
    print(res.text)
    js=json.loads(res.text)
    print(f"{js['query_elec_roominfo']['errmsg']} {js['query_elec_roominfo']['building']['building'] } {js['query_elec_roominfo']['room']['room'] }")

    input()