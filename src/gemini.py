import flet as ft
from google import genai
# from google.genai import types

from helper.get_diary import Diary
from helper.logger import Logger , LogLevel

# .envを読み込む
from dotenv import load_dotenv
import os

load_dotenv()

# Gemini APIクライアントの初期化
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

defult_prompt = """
基本的に前置きは不要です。
以下に入力された日記の内容を要約し、さらにその内容に基づいて励ましのコメントを日本語で一言で作成してください。
ユーザーが入力したコメントやTODOも考慮してください。
文字数にして70文字以内でお願いします。

日記のフォーマットは次の通りです。
日記の内容：<日記の内容>
コメント:<ユーザーが入力したコメント>
TODO: <ユーザーが入力したTODO>

出力フォーマットは次の通りです。
<励ましのコメント>　(70文字以内)

例外
意味のわからない日記や、日記の内容が非常に短い場合は、以下のように出力してください。
"すみませんｍ(_ _)ｍ よくわかりません。"
"""

def generate_ai_comment(diary: Diary) -> ft.Column:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=defult_prompt + "\n\n日記の内容：" + diary.activity_log+ "\nコメント:" + diary.comment + "\nTODO: " + diary.todo,
        config={
            "max_output_tokens": 256,
            "thinking_config": {
                "thinking_budget" : 0
            }
        }
    )

    res_text = response.text

    Logger.log(LogLevel.INFO, res_text)

    if not res_text:
        res_text = "AIコメントの生成に失敗しました。"
    else:
        res_text = res_text.strip()

    Logger.log_dump(LogLevel.INFO, f"Gemini API Response: {res_text}")

    return ft.Column(
        [
            ft.Text("AIからの最新コメント", size=16, weight="bold"),
            ft.Text(value=res_text, size=14),
        ],
        spacing=10,
    )

def generate_ai_comment_str(activity_log, comment , todo) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=defult_prompt + "\n\n日記の内容：" + activity_log+ "\nコメント:" + comment + "\nTODO: " + todo,
        config={
            "max_output_tokens": 256,
            "thinking_config": {
                "thinking_budget" : 0
            }
        }
    )

    res_text = response.text

    Logger.log(LogLevel.INFO, res_text)

    if not res_text:
        res_text = "AIコメントの生成に失敗しました。"
    else:
        res_text = res_text.strip()

    Logger.log_dump(LogLevel.INFO, f"Gemini API Response: {res_text}")

    return res_text


def test_gemini_api():
    dummy_diary = Diary(
        id=1,
        created_at="2023-10-01 10:00:00",
        updated_at="2023-10-01 10:00:00",
        activity_log="今日はとても良い天気でした。散歩に行ってリフレッシュできました。",
        comment="散歩は気持ちよかったです。",
        todo="明日は読書をする予定です。"
    )

    comment_text = generate_ai_comment(dummy_diary)
    print("Generated AI Comment:", comment_text.value)


if __name__ == "__main__":
    test_gemini_api()

