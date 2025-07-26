from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["book_catalog"]
books_collection = db["books"]

# Dummy book data
dummy_books = [
    {
        "username": "vanss",
        "title": "The AI Revolution",
        "author": "Elon Data",
        "genre": "Tech",
        "year": "2023",
        "description": "A dive into the future of artificial intelligence.",
        "cover_filename": "ai_revolution.jpg"
    },
    {
        "username": "vanss",
        "title": "Midnight Algorithms",
        "author": "Ada Byte",
        "genre": "Programming",
        "year": "2021",
        "description": "Tales of logic and bugs at 3AM.",
        "cover_filename": "midnight_algorithms.jpg"
    },
    {
        "username": "vanss",
        "title": "Design Patterns Unfolded",
        "author": "Grady Booch",
        "genre": "Software Engineering",
        "year": "2019",
        "description": "Understanding patterns in modern software design.",
        "cover_filename": "design_patterns.jpg"
    }
]

# Insert dummy books
books_collection.insert_many(dummy_books)

print("✅ Dummy books inserted for user: vanss")