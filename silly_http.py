import threading
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 使用 SillyTavern 的共享上下文
from extensions.server.utils import add_route
from modules.presets import get_active_preset
from modules.character import get_active_character
from modules.llm.proxy import send_prompt_to_llm
from modules.context import build_prompt

# FastAPI 实例
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/external/chat")
async def external_chat(req: Request):
    try:
        data = await req.json()
        user_msg = data.get("message", "")

        # 构建 prompt
        character = get_active_character()
        preset = get_active_preset()
        full_prompt = build_prompt(user_msg, preset, character)

        # 发送到 LLM 获取回复
        reply = await send_prompt_to_llm(full_prompt)

        return {"reply": reply}
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