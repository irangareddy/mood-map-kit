import json
import datetime
import uuid
import appwrite.exception
from appwrite.client import Client

from appwrite.permission import Permission
from appwrite.role import Role
from appwrite.services.databases import Databases
from appwrite.services.users import Users


####################################################################
# Utils
def try_except_decorator(location):
    """try except decorator"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                print(f"An error occurred at {location}: {exception}")

        return wrapper

    return decorator


################################################################
# HeatmapGenerator
class HeatmapGenerator:
    """Generates Heatmap data"""

    def __init__(self, json_data):
        """Constructor"""
        self.data = json.loads(json_data)
        self.date_range = []
        self.contributions = {}
        self.streak_count = 0

    @try_except_decorator(location="generate_date_range")
    def generate_date_range(self, num_days):
        """Generates a range of dates"""
        current_date = datetime.date.today()
        self.date_range = [
            str(current_date - datetime.timedelta(days=i)) for i in range(num_days)
        ]

    @try_except_decorator(location="update_contributions")
    def update_contributions(self):
        """Update the contributors"""
        self.contributions = {date: 0 for date in self.date_range}
        for doc in self.data["documents"]:
            created_at = (
                datetime.datetime.fromisoformat(doc["$createdAt"].rstrip("Z"))
                .date()
                .isoformat()
            )
            if created_at in self.contributions:
                self.contributions[created_at] += 1

    @try_except_decorator(location="calculate_streak_count")
    def calculate_streak_count(self):
        """Calculates the streak count"""
        current_streak = 0
        for count in self.contributions.values():
            if count > 0:
                current_streak += 1
                self.streak_count = max(self.streak_count, current_streak)
            else:
                current_streak = 0

    @try_except_decorator(location="generate_heatmap")
    def generate_heatmap(self, days):
        """Generates heatmap"""
        self.generate_date_range(days)
        self.update_contributions()
        self.calculate_streak_count()

    @try_except_decorator(location="create_json_object")
    def create_json_object(self):
        """Create a JSON object"""
        json_obj = {
            "heatmap": str(self.contributions),
            "streakCount": self.streak_count,
        }
        return json_obj


################################################################
# UserPreferences
class UserPreferences:
    """User preferences settings"""

    def __init__(self, user_id, users):
        """Create a new user preferences"""
        self.user_id = user_id
        self.users = users
        self.heatmap_id = None
        self.mood_analysis_id = None

    @try_except_decorator(location="get_user_preferences")
    def get_user_preferences(self):
        """Get user preferences"""
        preferences = self.users.get_prefs(self.user_id)
        self.heatmap_id = preferences.get("heatmap_id")
        self.mood_analysis_id = preferences.get("mood_analysis_id")
        return preferences

    @try_except_decorator(location="update_prefs")
    def update_prefs(self, prefs):
        """Update the preferences"""
        updated_preferences = self.users.update_prefs(user_id=self.user_id, prefs=prefs)
        return updated_preferences


########################################################################
# handle_heatmap_document
@try_except_decorator(location="handle_heatmap_document")
def handle_heatmap_document(
    databases,
    database_id,
    heatmap_collection_id,
    document_id,
    user_id,
    json_obj,
):
    """Function to handle document retrieval or creation"""

    try:
        existed_document = databases.get_document(
            database_id=database_id,
            collection_id=heatmap_collection_id,
            document_id=document_id,
        )
    except appwrite.exception.AppwriteException as exception:
        # Handle the exception here
        print(
            f"Document with the requested ID could not "
            f"be found. Creating a new document. {exception}"
        )
        existed_document = None

    if existed_document is not None:
        # Update the existing document
        heatmap_document_details = databases.update_document(
            database_id=database_id,
            collection_id=heatmap_collection_id,
            document_id=document_id,
            data=json.dumps(json_obj),
            permissions=[
                Permission.read(Role.user(user_id)),
                Permission.write(Role.user(user_id)),
                Permission.update(Role.user(user_id)),
                Permission.delete(Role.user(user_id)),
            ],
        )
    else:
        # Create a new document
        heatmap_document_details = databases.create_document(
            database_id=database_id,
            collection_id=heatmap_collection_id,
            document_id=document_id,
            data=json.dumps(json_obj),
            permissions=[
                Permission.read(Role.user(user_id)),
                Permission.write(Role.user(user_id)),
                Permission.update(Role.user(user_id)),
                Permission.delete(Role.user(user_id)),
            ],
        )
    return heatmap_document_details


@try_except_decorator(location="generate_document_id")
def generate_document_id(preferences):
    """Generates document id"""
    try:
        existed_document_id = preferences["heatmap_id"]
    except KeyError:
        existed_document_id = None

    if not existed_document_id:
        document_id = str(uuid.uuid4())
        # Save the document_id to preferences or perform any other desired action
    else:
        document_id = existed_document_id

    return document_id


def main(req, res):
    """main function"""
    payload = (
        req.payload or "No payload provided. Add custom data when executing function."
    )

    print("Execution started.")

    print(payload)
    try:
        print("Loading payload")
        payload = json.loads(payload)
    except ValueError:
        print("Error loading payload")
        print(json.loads(json.dumps(payload)))
    user_id = payload["userId"]
    print("Successfully loaded payload")

    # Create an instance of FunctionVariables
    function_vars = FunctionVariables(req)

    # Create an instance of AppwriteClient
    client = Client()
    databases = Databases(client)
    users = Users(client)

    (
        client.set_endpoint(function_vars.appwrite_function_endpoint)
        .set_project(function_vars.appwrite_function_project_id)
        .set_key(function_vars.secret_key)
    )

    # Create a new instance of the User Preferences object
    user_preferences = UserPreferences(user_id=user_id, users=users)
    preferences = user_preferences.get_user_preferences()
    print("Successfully loaded user preferences")

    document_id = generate_document_id(preferences)
    print("Successfully generated document id")

    print("Fetching collections.")
    _ = databases.list_collections(database_id=function_vars.database_id)

    # GET MOOD ENTRIES:
    print("Fetching mood entries.")
    mood_entries = databases.list_documents(
        database_id=function_vars.database_id,
        collection_id=function_vars.mood_entries_collection_id,
    )

    # GENERATE HEATMAP:
    print("Generating heatmap.")
    heatmap = HeatmapGenerator(json_data=json.dumps(mood_entries))
    heatmap.generate_heatmap(90)
    json_obj = heatmap.create_json_object()
    print("Generated heatmap.")
    heatmap_document_details = handle_heatmap_document(
        databases,
        function_vars.database_id,
        function_vars.heatmap_collection_id,
        document_id,
        user_id,
        json_obj,
    )
    print("Updated Document.")

    analytics_data = {
        "heatmap_id": heatmap_document_details["$id"],
    }

    updated_preferences = user_preferences.update_prefs(analytics_data)
    print("Updated User Preferences.")

    trigger = req.variables["APPWRITE_FUNCTION_TRIGGER"]

    print("Execution completed.")
    return res.json(
        {
            "message": "Successfully Generated Analysis",
            "trigger": trigger,
            "executedBy": user_id,
            "updated_preferences": updated_preferences,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


class FunctionVariables:
    """Function Variables"""

    def __init__(self, req):
        """Construct a new FunctionVariables"""
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
        """Returns a variable"""
        return self.req.variables.get(variable_name, default_message)


################################################################
# DEBUG ONLY
#
# import os
# from dotenv import load_dotenv
#
#
# class FunctionRequest:
#     """Function request"""
#     def __init__(self, payload, variables):
#         """Construct"""
#         self.payload = payload
#         self.variables = variables
#
#
# class FunctionResponse:
#     """Function response"""
#     def __init__(self):
#         """Construct"""
#         pass
#
#     def json(self, data):
#         return json.dumps(data)
#
#
# if __name__ == "__main__":
#     # Load environment variables from ..env file
#     load_dotenv()
#
#     req = FunctionRequest(
#         payload='{"userId":"64840f1b2824935b48fc","from":"mobile"}',
#         variables={
#             "SECRET_KEY": os.getenv("SECRET_KEY"),
#             "APPWRITE_DB_ID": os.getenv("APPWRITE_DB_ID"),
#             "MOOD_ENTRIES_COLLECTION_ID": os.getenv("MOOD_ENTRIES_COLLECTION_ID"),
#             "APPWRITE_FUNCTION_ENDPOINT": os.getenv("APPWRITE_FUNCTION_ENDPOINT"),
#             "APPWRITE_FUNCTION_PROJECT_ID": os.getenv("APPWRITE_FUNCTION_PROJECT_ID"),
#             "APPWRITE_FUNCTION_TRIGGER": os.getenv("APPWRITE_FUNCTION_TRIGGER"),
#             "HEATMAP_COLLECTION_ID": os.getenv("HEATMAP_COLLECTION_ID"),
#         },
#     )
#     res = FunctionResponse()
#     print(main(req, res))
#
# DEBUG END
