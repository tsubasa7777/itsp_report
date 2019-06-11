# 概要
* 使用言語 : Python
* CI : CircleCI
# 実装機能
* TODOの追加
* TODOの全件取得
* TODOを１件のみ取得
# 作成したTODO管理のHTTPサーバーの構成
まず、todo_server.pyを実行しサーバーを起動する。その後、サーバーはGETまたはPSOTリクエストを待ち続ける。サーバーがGETリクエストを受けとった時とPOSTリクエストを受けとった時、それぞれどのような処理を行うかについて分けて説明していく。
## GETリクエストを受けとった時
まず、リクエストのURLをパースする。http://localhost:8080/ 以降のパスを取得する。(http://localhost:8080/api/v1/event だと api/v1/eventの部分)
GETリクエストではこの部分がapi/v1/event(全件取得)かapi/v1/event/数字(ID指定取得)の2つ時のみ正常なレスポンスを行う。これら以外のリクエストだった場合、“Bad Request"をレスポンスとして返す。
全件取得のリクエスト時は、全てのTODOが格納されている配列data_arrayをそのまま全てリクエストとして返す。TODOが一件も格納されていない時であれば、“Not Found"をレスポンスとして返す。
ID指定取得リクエスト時は、api/v1/event/数字の「数字」と配列data_arrayに格納されている各TODOの「id」と比較する。マッチすれば、そのTODOをリクエストとして返す。マッチしない場合は、“Not Found"をレスポンスとして返す。
## POSTリクエストを受けとった時
まず、POSTリクエストの-dオプションで指定されたbody(TODO)の取得、そしてURLのパースを行う。URLはhttp://localhost:8080/api/v1/event の時のみ正常なレスポンスを返す。いれ以外は、“Bad Request"をレスポンスとして返す。
受け取ったTODOはJSON形式なので、扱いやすさのために辞書型に変換した。
TODOの要素として“deadline"、“title"、“memo"の3つが必ずあるかチェックする。どれか１つでもない場合は、“Bad Request"をレスポンスとして返す。
また、“deadline"に関しては、日付がRFC3339形式の文字列かどうかチェックする。このサーバーが受理する日付は“4桁の数字-2桁の数字-2桁の数字(T/t)2桁の数字:2桁の数字:2桁の数字(((+/-)2桁の数字:2桁の数字)/Z/z)"の形式に沿ったものである。RFC3339形式でない場合は、“Bad Request"をレスポンスとして返す。
以上のチェックを通過したTODOをid番号を付け加えて、配列data_arrayに格納する。
# CircleCIによるテスト結果
* TODOが1件もない時、全取得　→　Not Found(正常)
```
curl -X GET http://localhost:8080/api/v1/event
404 Not Found
```

* TODOが1件もない時、存在しないID指定取得→　Not Found(正常)
```
curl -X GET http://localhost:8080/api/v1/event/1
404 Not Found
```

* TODO登録(id:1)　→　登録成功(正常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11T14:00:00+09:00", "title":"1番目のTODO", "memo":""}' http://localhost:8080/api/v1/event
200 OK
{"status":"success","message":"registered","id":1}
```

* TODOが1件、全取得(正常)
```
curl -X GET http://localhost:8080/api/v1/event
200 OK
{"event":[
  {
    "id": 1,
    "deadline": "2019-06-11T14:00:00+09:00",
    "title": "1番目のTODO",
    "memo": ""
  }
]}
```

* TODOが1件、存在するID(id:1を指定)指定取得(正常)
```
curl -X GET http://localhost:8080/api/v1/event/1
200 OK
{
  "id": 1,
  "deadline": "2019-06-11T14:00:00+09:00",
  "title": "1番目のTODO",
  "memo": ""
}
```

* TODOが1件、存在しないID(id:５を指定)指定取得 →　Not Found(正常)
```
curl -X GET http://localhost:8080/api/v1/event/5
404 Not Found
```

* TODO登録(日付がRFC3339形式の文字列ではない)　→　登録失敗(異常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11T14:00:00", "title":"", "memo":""}' http://localhost:8080/api/v1/event
400 Bad Request
{"status":"failure","message":"invalid date format"}
```

* TODO登録(id:2)(日付におけるtime-numoffsetで”-”を使う)　→　登録成功(正常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11T14:00:00-09:00", "title":"2番目のTODO", "memo":"No.2"}' http://localhost:8080/api/v1/event
200 OK
{"status":"success","message":"registered","id":2}
```

* TODO登録(id:3)(日付におけるtime-offsetで"Z"を使う)　→　登録成功(正常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11T14:00:00Z", "title":"3番目のTODO", "memo":"Third"}' http://localhost:8080/api/v1/event
200 OK
{"status":"success","message":"registered","id":3}
```

* TODO登録(id:4)(日付におけるtime-offsetで"z"を使う)　→　登録成功(正常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11T14:00:00z", "title":"4番目のTODO", "memo":"for"}' http://localhost:8080/api/v1/event
200 OK
{"status":"success","message":"registered","id":4}
```

* TODO登録(id:5)(日付におけるdate-timeで"t"を使う)　→　登録成功(正常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11t14:00:00+09:00", "title":"5番目のTODO", "memo":"5"}' http://localhost:8080/api/v1/event
200 OK
{"status":"success","message":"registered","id":5}
```

* TODO登録("deadline"がない)　→　登録失敗(異常)
```
curl -X POST -H "Content-Type:application/json" -d '{"title":"レポート提出", "memo":""}' http://localhost:8080/api/v1/event
400 Bad Request
{"status":"failure","message":"invalid date format"}
```

* TODO登録("title"がない)　→　登録失敗(異常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11t14:00:00+09:00", "memo":""}' http://localhost:8080/api/v1/event
400 Bad Request
{"status":"failure","message":"invalid date format"}
```

* TODO登録("memo"がない)　→　登録失敗(異常)
```
curl -X POST -H "Content-Type:application/json" -d '{"deadline":"2019-06-11t14:00:00+09:00", "title":"レポート提出"}' http://localhost:8080/api/v1/event
400 Bad Request
{"status":"failure","message":"invalid date format"}
```

* TODOが5件、全取得(正常)
```
curl -X GET http://localhost:8080/api/v1/event
200 OK
{"event":[
  {
    "id": 1,
    "deadline": "2019-06-11T14:00:00+09:00",
    "title": "1番目のTODO",
    "memo": ""
  },
  {
    "id": 2,
    "deadline": "2019-06-11T14:00:00-09:00",
    "title": "2番目のTODO",
    "memo": "No.2"
  },
  {
    "id": 3,
    "deadline": "2019-06-11T14:00:00Z",
    "title": "3番目のTODO",
    "memo": "Third"
  },
  {
    "id": 4,
    "deadline": "2019-06-11T14:00:00z",
    "title": "4番目のTODO",
    "memo": "for"
  },
  {
    "id": 5,
    "deadline": "2019-06-11t14:00:00+09:00",
    "title": "5番目のTODO",
    "memo": "5"
  }
]}
```

* TODOが5件、存在するID(id:5を指定)指定取得(正常)
```
curl -X GET http://localhost:8080/api/v1/event/5
200 OK
{
  "id": 5,
  "deadline": "2019-06-11t14:00:00+09:00",
  "title": "5番目のTODO",
  "memo": "5"
}
```