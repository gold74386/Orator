from speechmodules.wakeword import PicoWakeWord
from speechmodules.speech2text import BaiduASR, AzureASR
from speechmodules.text2speech import BaiduTTS, Pyttsx3TTS, AzureTTS
from chatmodules.openai_chat_module import OpenaiChatModule
import struct
import requests

PICOVOICE_API_KEY = "wY0VT8DVVUP4K21nZQRsDRGBBbhAy+66zu6SxOxw5WMbpKWT0Vwcxw==" # 你的picovoice key
keyword_path = './speechmodules/Hey--Venus_en_windows_v2_1_0.ppn' # 你的唤醒词检测离线文件地址
Baidu_APP_ID = '32353381' # 你的百度APP_ID
Baidu_API_KEY = 'dlh6gQDLkpKWZKhgjxRGHo0p' # 你的百度API_KEY
Baidu_SECRET_KEY = 'j4IVX3UalUCOG6E6oyCIsgcHaser1xI6' # 你的百度SECRET_KEY
openai_api_key = "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"

AZURE_API_KEY = "3e1c960933fa4820bef175f62bad6133"
AZURE_REGION = "eastus"


def run(picowakeword, asr, tts, openai_chat_module):
    while True: # 需要始终保持对唤醒词的监听
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            picowakeword.stream.close()
            picowakeword.myaudio.terminate() # 需要对取消对麦克风的占用!
            print("嗯,主人我在,请讲！")
            tts.text_to_speech_and_play("嗯,主人我在,请讲！")
            while True:  # 进入一次对话session
                q = asr.speech_to_text()
                print(f'recognize_from_microphone, text={q}')
                if "退出" in q:  # 检测到关键词“退出”时退出对话
                    break
                else:
                    res = openai_chat_module.chat_with_origin_model(q)
                    print(res)
                    tts.text_to_speech_and_play('嗯'+res)
            print('本轮对话结束')
            tts.text_to_speech_and_play('嗯'+'主人，我退下啦！')

PICOVOICE_API_KEY = "wY0VT8DVVUP4K21nZQRsDRGBBbhAy+66zu6SxOxw5WMbpKWT0Vwcxw==" # 你的picovoice key
keyword_path = './speechmodules/Hey--Venus_en_windows_v2_1_0.ppn' # 你的唤醒词检测离线文件地址
Baidu_APP_ID = '32353381' # 你的百度APP_ID
Baidu_API_KEY = 'dlh6gQDLkpKWZKhgjxRGHo0p' # 你的百度API_KEY
Baidu_SECRET_KEY = 'j4IVX3UalUCOG6E6oyCIsgcHaser1xI6' # 你的百度SECRET_KEY
openai_api_key = "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"

AZURE_API_KEY = "3e1c960933fa4820bef175f62bad6133"
AZURE_REGION = "eastus"

def Orator():
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    asr = AzureASR(AZURE_API_KEY, AZURE_REGION)
    tts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    openai_chat_module = OpenaiChatModule(openai_api_key)
    try:
        run(picowakeword, asr, tts, openai_chat_module)
    except KeyboardInterrupt:
        if picowakeword.porcupine is not None:
            picowakeword.porcupine.delete()
            print("Deleting porc")
        if picowakeword.stream is not None:
            picowakeword.stream.close()
            print("Closing stream")
        if picowakeword.myaudio is not None:
            picowakeword.myaudio.terminate()
            print("Terminating pa")
        exit(0)
    finally:
        if picowakeword.porcupine is not None:
            picowakeword.porcupine.delete()
            print("Deleting porc")
        if picowakeword.stream is not None:
            picowakeword.stream.close()
            print("Closing stream")
        if picowakeword.myaudio is not None:
            picowakeword.myaudio.terminate()
            print("Terminating pa")
        Orator()

if __name__ == "__main__":
    Orator()