import json
import argparse

from bottle import route, run, response, request
from transformers import AutoModel, AutoTokenizer

@route('/api/chat', method='POST')
def index():
    data = request.json
    prompt = data.get('prompt')
    max_length = data.get('max_length')
    if max_length is None:
        max_length = 2048
    top_p = data.get('top_p')
    if top_p is None:
        top_p = 0.7
    temperature = data.get('temperature')
    if temperature is None:
        temperature = 0.9
    history = data.get('history')
    # history = [
    #     {
    #         "role": "user",
    #         "content": "hello"
    #     },
    #     {
    #         "role": "AI",
    #         "content": "hello, can I help you?"
    #     }
    # ]
    history_formatted = None
    if history is not None:
        history_formatted = []
        tmp = []
        for i, old_chat in enumerate(history):
            if len(tmp) == 0 and old_chat['role'] == "user":
                tmp.append(old_chat['content'])
            elif old_chat['role'] == "AI":
                tmp.append(old_chat['content'])
                history_formatted.append(tuple(tmp))
                tmp = []
            else:
                continue
    result, history = model.chat(tokenizer, prompt, history_formatted, max_length=max_length, top_p=top_p,
                                 temperature=temperature)
    # 将JSON对象转换为字符串
    json_data = json.dumps({
        "data": result
    })
    # 设置响应头部的Content-Type为application/json
    response.content_type = 'application/json'
    # 返回JSON字符串
    return json_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple API server for ChatGLM-6B')
    parser.add_argument('--device', '-d', help='使用设备，cpu或cuda:0等', default='cpu')
    parser.add_argument('--quantize', '-q', help='量化等级。可选值：16，8，4', default=16)
    parser.add_argument('--host', '-H', help='监听Host', default='127.0.0.1')
    parser.add_argument('--port', '-P', help='监听端口号', default=8080)
    args = parser.parse_args()
    model_name = "THUDM/chatglm-6b"
    quantize = args.quantize
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = None
    if args.device == 'cpu':
        if quantize == 8:
            print('cpu模式下量化等级只能是16或4，使用4')
            model_name = "THUDM/chatglm-6b-int4"
        elif quantize == 4:
            model_name = "THUDM/chatglm-6b-int4"
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True).float()
    else:
        if quantize == 16:
            model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().cuda()
        else:
            model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().quantize(quantize).cuda()
    model = model.eval()
    run(host=args.host, port=args.port)
