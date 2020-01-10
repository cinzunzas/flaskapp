import requests


class Connection:
    def post(self, url, args, multipart=False):
        response = {
            'code': '',
            'body': ''
        }
        if multipart:
            boundary = "--**myboundary**--"
            multipartPostData = ""
            for key, value in args.items():
                multipartPostData += "--" + boundary + "\r\nContent-Disposition: form-data; name=\"" + key + "\"\r\n\r\n" + value + "\r\n";
            multipartPostData += "--" + boundary + "--"

            headers = {
                'Content-Type': 'multipart/form-data; boundary=' + boundary,
                'Expect': ''
            }
            r = requests.post(
                url,
                headers=headers,
                data=multipartPostData,
                timeout=120
            )
            # TODO: Loggear response
            if r.status_code is not 204:
                response['code'] = r.status_code
                response['body'] = "nook"
            else:
                response['code'] = 200
                response['body'] = "ok"
        else:
            r = request.post(url, data=args)
            response['code'] = r.status_code
            response['body'] = r.content.decode('utf-8')
            return response
        return response
