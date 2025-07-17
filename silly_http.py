import threading
import traceback
from fastapi import FastAPI, Request
import uvicorn

# 创建 FastAPI 实例
app = FastAPI()

@app.post("/external/chat")
async def external_chat(req: Request):
    try:
        data = await req.json()
        user_msg = data.get("message", "")

        # 这里只是一个简单的响应，你可以根据需要修改为与 SillyTavern 交互的代码
        # 示例：直接返回输入的消息
        return {"reply": f"酒馆回复：{user_msg}"}

    except Exception as e:
        print("[silly_http] Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# 插件初始化函数
def setup():
    def run():
        uvicorn.run(app, host="0.0.0.0", port=11435)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print("[silly_http] External HTTP API server running at http://localhost:11435")
