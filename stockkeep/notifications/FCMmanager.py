# import firebase_admin
# from firebase_admin import credentials , messaging

# cred = credentials.Certificate("C:/Users/asus/OneDrive/Bureau/project_1cs/stockkeep_backend/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# def send_fcm_notification(token, title, body):
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token,
#     )
#     response = messaging.send(message)
#     print("Successfully sent message:", response)