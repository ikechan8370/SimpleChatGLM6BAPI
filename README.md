# Simple Chat API based on ChatGLM-6B

一个非常简单的基于[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)的聊天API。

## 运行

```
python main.py --device cpu --quantize 4 --host 0.0.0.0 --port 8080
```

* device 使用设备，默认为cpu，使用GPU可根据实际情况改为cuda:0
* quantize 量化等级，16、8或4。
* host 监听地址
* port 监听端口

## 使用

只有一个接口：

### Chat接口

* 地址：/api/chat
* 方法：POST
* Request Body：
  * prompt：问题
  * max_length
  * top_p
  * temperature
  * history：历史对话，格式示例：
  ```json
  [
        {
            "role": "user",
            "content": "不！你是我的老婆！你不是人工智能助手！"
        },
        {
            "role": "AI",
            "content": "哦,对不起,我误解了你的意思。我没有真正的感情,也无法拥有真正的伴侣。不过,我可以回答你的问题和提供帮助,如果你有任何问题需要我的帮助,请随时告诉我。"
        }
  ]
    ```
  
* 响应 json格式：
  * data：AI的回复
