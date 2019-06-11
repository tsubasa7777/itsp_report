# 作成したTODO管理のHTTPサーバーの概要
まず、todo_server.pyを実行しサーバーを起動する。その後、サーバーはGETまたはPSOTリクエストを待ち続ける。GETリクエストを受けとった時とPOSTリクエストを受けとった時の２つに分けて説明していく。
## GETリクエストを受けとった時
まず、リクエストのURLをパースする。http://localhost:8080/ 以降のパスを取得する。(http://localhost:8080/api/v1/event だと api/v1/eventの部分)
GETリクエストではこの部分がapi/v1/event(全件取得)かapi/v1/event/数字(ID指定取得)の2つ時のみ正常なレスポンスを行う。これら以外のリクエストだった場合、“Bad Request"をレスポンスとして返す。
全件取得のリクエスト時は、全てのTODOが格納されている配列data_arrayをそのまま全てリクエストとして返す。TODOが一件も格納されていない時であれば、“Not Found"をレスポンスとして返す。
ID指定取得リクエスト時は、api/v1/event/数字の「数字」と配列data_arrayに格納されている各TODOの「id」と比較する。マッチすれば、そのTODOをリクエストとして返す。マッチしない場合は、“Not Found"をレスポンスとして返す。
## POSTリクエストを受けとった時
まず、POSTリクエストの-dオプションで指定されたbodyの取得、そしてURLのパースを行う。URLはhttp://localhost:8080/api/v1/event の時のみ正常なレスポンスを返す。いれ以外は、“Bad Request"をレスポンスとして返す。