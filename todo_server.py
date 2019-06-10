from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import re

counter = 0  # idを記憶する変数
data_array = []  # todoを格納する配列


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # リクエスト解析
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        # URLチェック
        try:
            if path_elements[0] != 'api':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return

            if path_elements[1] != 'v1':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return

            if path_elements[2] != 'event':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return
        except:
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return

        # 全件取得のリクエスト
        if len(path_elements) == 3:
            try:
                if not data_array:
                    self.wfile.write("404 Not Found\n".encode("utf-8"))
                    return
                self.wfile.write("200 OK\n".encode("utf-8"))
                self.wfile.write(("{\"event\":" + (str(json.dumps(data_array, ensure_ascii=False, indent=2))) + "}\n").encode("utf-8"))
            except Exception as e:
                print(e)
                return

        # id指定取得のリクエスト
        if len(path_elements) == 4:
            try:
                if not data_array:
                    self.wfile.write("404 Not Found\n".encode("utf-8"))
                    return
                get_id = int(path_elements[3])
                for data in data_array:
                    if data['id'] == get_id:
                        self.wfile.write("200 OK\n".encode("utf-8"))
                        self.wfile.write(((str(json.dumps(data, ensure_ascii=False, indent=2))) + "\n").encode("utf-8"))
                        return
                self.wfile.write("404 Not Found\n".encode("utf-8"))
                return
            except Exception as e:
                print(e)
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return

        # 形式が間違っているリクエスト
        if (len(path_elements) <= 2) or (len(path_elements) >= 5):
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return

    def do_POST(self):
        # リクエスト解析
        content_len = int(self.headers.get("content-length"))
        request_body = self.rfile.read(content_len).decode("utf-8")
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        # URLチェック
        if len(path_elements) != 3:
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return
        try:
            if path_elements[0] != 'api':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return

            if path_elements[1] != 'v1':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return

            if path_elements[2] != 'event':
                self.wfile.write("400 Bad Request\n".encode("utf-8"))
                self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
                return
        except Exception as e:
            print(e)
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return

        # todoを取り込む(JSON→辞書式)
        global counter, data_dict
        key_array = []
        data = json.loads(request_body)
        for key in data:
            key_array.append(key)

        # "deadline","title","memo"の3つ以外に誤った属性がないか確認
        if len(key_array) != 3:
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return

        # 日付がRFC3339形式の文字列かどうか判定
        value_array = []
        for value in data.values():
            value_array.append(value)
        match_object = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}(T|t)[0-9]{2}:[0-9]{2}:[0-9]{2}((\+|-)[0-9]{2}:[0-9]{2}|Z|z)", value_array[0])
        try:
            if len(value_array[0]) == match_object.end():
                pass
        except Exception as e:
            print(e)
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            return

        try:
            if "deadline" == key_array[0]:  # 形式のチェック
                if "title" == key_array[1]:  # 形式のチェック
                    if "memo" == key_array[2]:  # 形式のチェック
                        counter += 1
                        self.wfile.write("200 OK\n".encode("utf-8"))
                        self.wfile.write(("{\"status\":\"success\",\"message\":\"registered\",\"id\":"+str(counter)+"}\n").encode("utf-8"))
                        data_dict = {"id": counter}
                        data_dict.update(data)
                        data_array.append(data_dict)
                        return
        except Exception as e:
            print(e)
            self.wfile.write("400 Bad Request\n".encode("utf-8"))
            self.wfile.write("{\"status\":\"failure\",\"message\":\"invalid date format\"}\n".encode("utf-8"))
            self.wfile.write(e.encode("utf-8"))
            return


def main():
    server = HTTPServer(('', 8080), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
