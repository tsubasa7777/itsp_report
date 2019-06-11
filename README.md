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