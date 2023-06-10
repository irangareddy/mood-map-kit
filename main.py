import json


# import datetime
# import uuid
# import appwrite.exception
from appwrite.client import Client

# from appwrite.permission import Permission
# from appwrite.role import Role
from appwrite.services.databases import Databases
from appwrite.services.users import Users


# class HeatmapGenerator:
#     def __init__(self, json_data):
#         self.data = json.loads(json_data)
#         self.date_range = []
#         self.contributions = {}
#         self.streak_count = 0
#
#     def generate_date_range(self, num_days):
#         current_date = datetime.date.today()
#         self.date_range = [str(current_date - datetime.timedelta(days=i)) for i in range(num_days)]
#
#     def update_contributions(self):
#         self.contributions = {date: 0 for date in self.date_range}
#         for doc in self.data["documents"]:
#             created_at = datetime.datetime.fromisoformat(doc['$createdAt'].rstrip('Z')).date().isoformat()
#             if created_at in self.contributions:
#                 self.contributions[created_at] += 1
#
#     def calculate_streak_count(self):
#         current_streak = 0
#         for count in self.contributions.values():
#             if count > 0:
#                 current_streak += 1
#                 self.streak_count = max(self.streak_count, current_streak)
#             else:
#                 current_streak = 0
#
#     def generate_heatmap(self, days):
#         self.generate_date_range(days)
#         self.update_contributions()
#         self.calculate_streak_count()
#
#     def create_json_object(self):
#         json_obj = {
#             "heatmap": str(self.contributions),
#             "streakCount": self.streak_count
#         }
#         return json_obj
#
#
class UserPreferencesRanga:
    def __init__(self, user_id, users):
        self.user_id = user_id
        self.users = users
        self.heatmap_id = None
        self.mood_analysis_id = None

    def get_user_preferences(self):
        preferences = self.users.get_prefs(self.user_id)
        self.heatmap_id = preferences.get("heatmap_id")
        self.mood_analysis_id = preferences.get("mood_analysis_id")
        return preferences


# Function to fetch user preferences
def get_user_preferences(users, user_id):
    user_preferences = UserPreferencesRanga(user_id=user_id, users=users)
    preferences = user_preferences.get_user_preferences()
    return preferences


#
# # Function to handle document retrieval or creation
# def handle_heatmap_document(databases, database_id, heatmap_collection_id, preferences, payload, json_obj):
#     document_id = str(uuid.uuid4())  # Generate a new UUID for the document_id parameter
#
#     if 'heatmap_document_id' in preferences:
#         heatmap_document_id = preferences['heatmap_document_id']
#         try:
#             existed_document = databases.get_document(database_id=database_id,
#                                                       collection_id=heatmap_collection_id,
#                                                       document_id=heatmap_document_id)
#         except appwrite.exception.AppwriteException as exception:
#             # Handle the exception here
#             print(f"Document with the requested ID could not be found. Creating a new document. {exception}")
#             existed_document = None  # Set existed_document to None to indicate that it doesn't exist
#     else:
#         heatmap_document_id = document_id
#         existed_document = None  # Set existed_document to None to indicate that it doesn't exist
#
#     if existed_document is not None:
#         # Update the existing document
#         heatmap_document_details = databases.update_document(database_id=database_id,
#                                                              collection_id=heatmap_collection_id,
#                                                              document_id=heatmap_document_id,
#                                                              data=json.dumps(json_obj),
#                                                              permissions=[
#                                                                  Permission.read(Role.user(payload['userId'])),
#                                                                  Permission.write(Role.user(payload['userId'])),
#                                                                  Permission.update(Role.user(payload['userId'])),
#                                                                  Permission.delete(Role.user(payload['userId'])),
#                                                              ])
#     else:
#         # Create a new document
#         heatmap_document_details = databases.create_document(database_id=database_id,
#                                                              collection_id=heatmap_collection_id,
#                                                              document_id=heatmap_document_id,
#                                                              data=json.dumps(json_obj),
#                                                              permissions=[
#                                                                  Permission.read(Role.user(payload['userId'])),
#                                                                  Permission.write(Role.user(payload['userId'])),
#                                                                  Permission.update(Role.user(payload['userId'])),
#                                                                  Permission.delete(Role.user(payload['userId'])),
#                                                              ])
#     return heatmap_document_details


# Main function
# def main(req, res):
# try:
#     secret_key = req.variables.get(
#         'SECRET_KEY',
#         'SECRET_KEY variable not found. You can set it in Function settings.'
#     )
#

#

#
#     preferences = {}

#
#
#     print("Fetching collections.")
#     _ = databases.list_collections(database_id=database_id)
#     # _ = databases.delete_collection(database_id=database_id,
#     #                                 collection_id=heatmap_collection_id)
#
#     # GET MOOD ENTRIES:
#     print("Fetching mood entries.")
#     mood_entries = databases.list_documents(
#         database_id=database_id,
#         collection_id=mood_entries_collection_id
#     )
#
#     # GENERATE HEATMAP:
#     print("Generating heatmap.")
#     heatmap = HeatmapGenerator(json_data=json.dumps(mood_entries))
#     heatmap.generate_heatmap(90)
#     json_obj = heatmap.create_json_object()
#
#     heatmap_document_details = handle_heatmap_document(databases, database_id, heatmap_collection_id, preferences,
#                                                        payload, json_obj)
#
#     analytics_data = {
#         "heatmap_document_id": heatmap_document_details['$id']
#     }
#     result = users.update_prefs(user_id=user_id, prefs=analytics_data)
#
#     print("Execution completed.")
#
# except appwrite.exception.AppwriteException as exception:
#     print(f'ERROR at getting preferences {exception}')
# except Exception as exception:
#     print(f'ERROR at other preferences {exception}')

# return res(json.dumps({'documents': json_obj,
#                        'heatmap_document_id': heatmap_document_details['$id'],
#                        'updated_user_preferences': result}))

# return res(json.dumps({'status': trigger}))

#
# import os
# from dotenv import load_dotenv
#
#
# class FunctionRequest:
#     def __init__(self, payload, variables):
#         self.payload = payload
#         self.variables = variables
#
#
# class FunctionResponse:
#     def __init__(self, json):
#         self.json = json
#
#
# if __name__ == '__main__':
#     # Load environment variables from ..env file
#     load_dotenv()
#
#     req = FunctionRequest(payload="{\"userId\":\"64840f1b2824935b48fc\",\"from\":\"mobile\"}", variables={
#         'SECRET_KEY': os.getenv('SECRET_KEY'),
#         'APPWRITE_DB_ID': os.getenv('APPWRITE_DB_ID'),
#         'MOOD_ENTRIES_COLLECTION_ID': os.getenv('MOOD_ENTRIES_COLLECTION_ID'),
#         'APPWRITE_FUNCTION_ENDPOINT': os.getenv('APPWRITE_FUNCTION_ENDPOINT'),
#         'APPWRITE_FUNCTION_PROJECT_ID': os.getenv('APPWRITE_FUNCTION_PROJECT_ID'),
#         'APPWRITE_FUNCTION_TRIGGER': os.getenv('APPWRITE_FUNCTION_TRIGGER'),
#         'HEATMAP_COLLECTION_ID': os.getenv('HEATMAP_COLLECTION_ID'),
#     })
#     main(req, print)


def main(req, res):
    payload = (
        req.payload or "No payload provided. Add custom data when executing function."
    )

    print("Execution started.")
    trigger = req.variables["APPWRITE_FUNCTION_TRIGGER"]

    print(payload)
    try:
        print("Loading payload")
        payload = json.loads(payload)
    except ValueError:
        print("Error loading payload")
        print(json.loads(json.dumps(payload)))
    print(type(payload))
    user_id = payload["userId"]
    print(user_id)

    # Create an instance of FunctionVariables
    function_vars = FunctionVariables(req)

    client = Client()
    databases = Databases(client)
    users = Users(client)

    (
        client.set_endpoint(function_vars.appwrite_function_endpoint)
        .set_project(function_vars.appwrite_function_project_id)
        .set_key(function_vars.secret_key)
    )

    preferences = get_user_preferences(users, user_id)
    print(preferences)

    analytics_data = {
        "heatmap_id": "heatmap_document_details",
    }

    updated_preferences = users.update_prefs(user_id=user_id, prefs=analytics_data)

    print("Execution completed.")

    trigger = req.variables["APPWRITE_FUNCTION_TRIGGER"]

    return res.json(
        {
            "message": "Loaded Client, Users, Databases",
            "payload": payload,
            "trigger": trigger,
            "user_id": user_id,
            "preferences": preferences,
            "updated_preferences": updated_preferences,
            "secretKey": function_vars.secret_key,
            "databaseId": function_vars.database_id,
            "moodEntriesCollectionId": function_vars.mood_entries_collection_id,
            "heatmapCollectionId": function_vars.heatmap_collection_id,
        }
    )


class FunctionVariables:
    def __init__(self, req):
        self.req = req
        self.appwrite_function_endpoint = self.get_variable(
            "APPWRITE_FUNCTION_ENDPOINT",
            "APPWRITE_FUNCTION_ENDPOINT variable not found. You can set it in Function settings.",
        )
        self.appwrite_function_project_id = self.get_variable(
            "APPWRITE_FUNCTION_PROJECT_ID",
            "APPWRITE_FUNCTION_PROJECT_ID variable not found. You can set it in Function settings.",
        )
        self.secret_key = self.get_variable(
            "SECRET_KEY",
            "SECRET_KEY variable not found. You can set it in Function settings.",
        )
        self.database_id = self.get_variable(
            "APPWRITE_DB_ID",
            "APPWRITE_DB_ID variable not found. You can set it in Function settings.",
        )
        self.mood_entries_collection_id = self.get_variable(
            "MOOD_ENTRIES_COLLECTION_ID",
            "MOOD_ENTRIES_COLLECTION_ID variable not found. You can set it in Function settings.",
        )
        self.heatmap_collection_id = self.get_variable(
            "HEATMAP_COLLECTION_ID",
            "HEATMAP_COLLECTION_ID variable not found. You can set it in Function settings.",
        )

    def get_variable(self, variable_name, default_message):
        return self.req.variables.get(variable_name, default_message)
