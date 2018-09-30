import json

def json_format(func):
    def res(data = []):
        data = func()
        re_data = json.dumps({"data": data})
        return re_data
    return res

class RemoteFunction(object):

    @json_format
    def a(data = []):
        return "a"

def build_js():
    remote_dict = RemoteFunction.__dict__
    # 初始化 ws链接
    remote_js = """
window.remote = {
    __init__: (url) => {
        var self = window.remote;
        self.ws_connect = new WebSocket(url + "/func");
        self.ws_connect.onopen = () => {console.log("Open Remote Func Success~")}
        self.ws_connect.onmessage = (res) => {console.log(res);}
        self.ws_connect.onclose = () => {setTimeout(() => {self.__init__(url)}, 3000)}
    },
    ws_connect: undefined,
    waitForValue: (obj, value) => {
        while(true){
            if(obj === value){
                return;
            }
        }
    },
    info_handler: {},

    """
    for key in remote_dict:
        if key.find("__") >= 0:
            continue
        remote_js += """
    %s :async (data, recall) => {
        var self = window.remote;
        if(!self.info_handler.hasOwnProperty("%s")){
            self.info_handler["%s"] = null
        }
        if(self.info_handler["%s"] != null){
            await self.waitForValue(self.info_handler["%s"], null);
        }
        self.ws_connect.send("%s " + data)
        self.info_handler["%s"] = recall
    },
        """%(key, key, key, key, key, key, key)
    remote_js += """
}
    """
    return remote_js

if __name__ == "__main__":
    remote_js = build_js()
    open("../template/netnet/static/js/remote.js", "w").write(remote_js)