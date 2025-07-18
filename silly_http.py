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

        # 打印调试信息，确认是否接收到请求
        print(f"Received message: {user_msg}")

        # 返回简单的回复
        return {"reply": f"酒馆回复：{user_msg}"}
        
    except Exception as e:
        print("[silly_http] Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# 插件初始化函数
def setup():
    def run():
        uvicorn.run(app, host="0.0.0.0", port=11435)

    print("[silly_http] Setting up API server...")  # 插件启动信息
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print("[silly_http] External HTTP API server running at http://localhost:11435")
