from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage
from linebot.exceptions import InvalidSignatureError
from fastapi import Request
import os, requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from utils.websocket import websocket_manager
from model import group_bot, group_member_bot, member_bot, message
import asyncio
load_dotenv()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))  
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# line_kg_ai = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN_KGAI"))  
# handler_kg_ai = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET_KGAI"))

DIFY_API_KEY = os.getenv("DIFY_MODEL_KEY")
DIFY_URL = os.getenv("DIFY_URL_KEY")

async def webhook(request: Request):
    
    signature = request.headers.get("X-Line-Signature")
    body = (await request.body()).decode("utf-8")

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Invalid LINE signature")
        print("Signature header:", signature)
        print("Webhook error", e)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    chat_type = event.source.type
    text = event.message.text
    reply_token = event.reply_token
    print("Received message:", event)
    utc_date = datetime.fromtimestamp(event.timestamp / 1000, tz=timezone.utc)
    kh_date = utc_date.astimezone(timezone(timedelta(hours=7)))
    
    group_id = None
    group_name = None
    user_name = None
    
    payload = {
        "inputs": {
            "cus_question": text,
            "web_name": "",
            "asker_name": user_name,
            "lang": "EN",
            "csname": "",
            "cscnname": "",
            "reply_str": "",
            "nowaday": kh_date.strftime("%Y-%m-%d %H:%M:%S"),
            "check_weather": 0,
            "img_url": "",
            "username": user_name,
        },
        "query": text,
        "response_mode": "blocking",
        "user": user_id
    }
    
    if chat_type == "group":
        group_id = event.source.group_id
        members = line_bot_api.get_group_member_profile(group_id, user_id)
        user_name = members.display_name
        group_summary = line_bot_api.get_group_summary(group_id)
        group_name = group_summary.group_name
        answer = ask_document(payload)
    else:
        profile = line_bot_api.get_profile(user_id)
        user_name = profile.display_name
        answer = ask_document(payload)
        
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=answer)
    )
    
    data = {
        "date_time": kh_date.strftime("%Y-%m-%d %H:%M:%S"),
        "chat_type": chat_type,
        "group_id": group_id,
        "group_name": group_name,
        "user_id": user_id,
        "user_name": user_name,
        "question": text,
        "answer": answer
    }
    
    
    message(
        user_id=user_id,
        user_name=user_name,
        group_id=group_id,
        group_name=group_name,
        question=text,
        answer=answer,
        date_time=kh_date.strftime("%Y-%m-%d %H:%M:%S"),
        chat_type=chat_type
        
    )
    asyncio.create_task(websocket_manager.broadcast(data))

    
def ask_document(payload: dict):
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    # payload = {
    #     "inputs": {
    #         "question": question
    #     },
    #     "response_mode": "blocking",
    #     "user": user_id
    # }
    
    # payload = {
    #     "inputs": {
    #         "cus_question": question,
    #         "web_name": "",
    #         "asker_name": "",
    #         "lang": "",
    #         "csname": "",
    #         "cscnname": "",
    #         "reply_str": "",
    #         "nowaday": "",
    #         "check_weather": "",
    #         "img_url": "",
    #         "username": "",
    #     },
    #     "query": question,
    #     "response_mode": "blocking",
    #     "user": user_id
    # }

    res = requests.post(DIFY_URL, json=payload, headers=headers, timeout=40)
    res.raise_for_status()

    data = res.json()
    
    return data["answer"]


# async def webhook(request: Request):
    
#     signature = request.headers.get("X-Line-Signature")
#     body = (await request.body()).decode("utf-8")

#     try:
#         handler_kg_ai.handle(body, signature)
#     except Exception as e:
#         print("Invalid LINE signature")
#         print("Signature header:", signature)
#         print("Webhook error", e)

#     return "OK"

# @handler_kg_ai.add(MessageEvent, message=TextMessage)
# def handle_text_message(event):
#     user_id = event.source.user_id
#     chat_type = event.source.type
#     text = event.message.text
#     reply_token = event.reply_token
#     print("Received message:", event)
#     utc_date = datetime.fromtimestamp(event.timestamp / 1000, tz=timezone.utc)
#     kh_date = utc_date.astimezone(timezone(timedelta(hours=7)))
    
#     group_id = None
#     group_name = None
#     user_name = None
    
#     payload = {
#         "inputs": {
#             "cus_question": text,
#             "web_name": "",
#             "asker_name": user_name,
#             "lang": "EN",
#             "csname": "",
#             "cscnname": "",
#             "reply_str": "",
#             "nowaday": kh_date.strftime("%Y-%m-%d %H:%M:%S"),
#             "check_weather": 0,
#             "img_url": "",
#             "username": user_name,
#         },
#         "query": text,
#         "response_mode": "blocking",
#         "user": user_id
#     }
    
#     if chat_type == "group":
#         group_id = event.source.group_id
#         members = line_bot_api.get_group_member_profile(group_id, user_id)
#         user_name = members.display_name
#         group_summary = line_bot_api.get_group_summary(group_id)
#         group_name = group_summary.group_name
#         answer = ask_document(payload)
#     else:
#         profile = line_bot_api.get_profile(user_id)
#         user_name = profile.display_name
#         answer = ask_document(payload)
        
#     line_kg_ai.reply_message(
#         reply_token,
#         TextSendMessage(text=answer)
#     )
    
#     data = {
#         "date_time": kh_date.strftime("%Y-%m-%d %H:%M:%S"),
#         "chat_type": chat_type,
#         "group_id": group_id,
#         "group_name": group_name,
#         "user_id": user_id,
#         "user_name": user_name,
#         "question": text,
#         "answer": answer
#     }
    
#     asyncio.create_task(websocket_manager.broadcast(data))
    