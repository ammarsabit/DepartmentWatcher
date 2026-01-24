import requests
import time
import telebot # pip install pyTelegramBotAPI
import threading
import os

login_credential = {
    "user_name": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD")
}

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

program = ""
bot = telebot.TeleBot(telegram_bot_token)

def login():
    login_url = "https://estudent.astu.edu.et/api/auth/sign_in"
    response = requests.post(login_url, json=login_credential)

    return response

def check_update(access_token, client, uid):
    graphql_url = "https://estudent.astu.edu.et/api/graphql"

    query = """
        query getPerson($id: ID!) {
            getPerson(id: $id) {
                applicant {
                    student {
                        program {
                        name
                        }
                    }
                }
            }
        }
    """

    headers = {
        "Access-Token": access_token,
        "Client": client,
        "Uid": uid
    }

    payload = {
        "operationName":"getPerson",
        "variables":{"id":122},
        "query": query}

    response = requests.post(graphql_url, json=payload, headers=headers)
    data = response.json().get("data")
    if not data:
        return None

    program_name = data["getPerson"]["applicant"]["student"]["program"]["name"]
    return program_name

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🎉 Welcome to ASTU's Department Release Watcher! We’ll notify you within 15 minutes once your department is released.")

    try:
        with open("bot_users.txt", "r") as file:
            users_id = file.readlines()
            for user_id in users_id:
                if user_id.strip() == str(chat_id):
                    return 
                
            with open("bot_users.txt", "a") as file:
                file.write(f"{chat_id}\n")
                
    except(FileNotFoundError):
        with open("bot_users.txt", "w") as file:
            file.write(f"{chat_id}\n")
                     
def botNotify():
    with open("bot_users.txt", "r") as file:
        users_id = file.readlines()
        for user_id in users_id:
            bot.send_message(user_id.strip(), "🎊 Congratulations! Your department has been released. Go check it on your student portal now!")

if __name__ == "__main__":
    response = None
    token_expiry = 0

    threading.Thread(target=bot.infinity_polling, daemon=True).start() # Telegram bot is listening on different thread so that it wont be blocked by the main thread 
    
    while True:
        if (time.time() > token_expiry):
            response = login()
            token_expiry = int(response.headers.get("expiry")) # Epoch time

        if response.status_code == 401:
            print("Invalid credential") 

        elif response.status_code != 200:
            print("something went wrong")
        else:
            access_token = response.headers.get("access-token")
            client = response.headers.get("client")
            uid = response.headers.get("uid")

            program_update = check_update(access_token, client, uid)
            if program_update is None:
                print("Failed to fetch program. Retrying...")
                continue

            elif (program == ""):
                program = program_update

            elif program != program_update:
                print("Department release detected!")
                print(f"Your department is {program_update}")
                botNotify()
                break

        time.sleep(900) # 15' of gap  
