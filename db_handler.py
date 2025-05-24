import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["TicketProject"]

# Collections
ticket_collection = db["tickets"]
guide_collection = db["guides"]
label_collection = db["labels"]

# ---------- TICKETS ----------
def save_ticket(data):
    ticket_collection.insert_one(data)

def get_all_tickets():
    return list(ticket_collection.find().sort("_id", -1))

# ---------- GUIDES ----------
def add_or_update_guide(label, data):
    guide_collection.update_one({"label": label}, {"$set": data}, upsert=True)

def get_guide_by_label(label):
    return guide_collection.find_one({"label": label})

def get_all_guides():
    return list(guide_collection.find())

# ---------- LABELS ----------
def get_all_labels():
    return list(label_collection.find({}, {"_id": 0}))

def add_label(name, description=""):
    label_collection.update_one(
        {"name": name},
        {"$set": {"name": name, "description": description}},
        upsert=True
    )

def remove_label(name):
    label_collection.delete_one({"name": name})
