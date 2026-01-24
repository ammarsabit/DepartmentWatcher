import requests

with open("credentials.txt", "r") as file:
    content = file.readlines()
    crendential = {
        "user_name": content[0].split("=")[1].strip(),
        "password": content[1].split("=")[1].strip(),
        "telegram_bot_token": content[2].split("=")[1].strip()
    }

def login():
    login_url = "https://estudent.astu.edu.et/api/auth/sign_in"
    response = requests.post(login_url, json=crendential)

    return response

def check_update(access_token, client, uid):
    graphql_url = "https://estudent.astu.edu.et/api//graphql"

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
    return response.json()["data"]["getPerson"]["applicant"]["student"]["program"]["name"]


if __name__ == "__main__":
    login = login()
    if login.status_code == 401:
        print("Invalid credential") 

    elif login.status_code != 200:
        print("something went wrong")
    else:
        access_token = login.headers.get("access-token")
        client = login.headers.get("client")
        uid = login.headers.get("uid")

        print(check_update(access_token, client, uid))
    

