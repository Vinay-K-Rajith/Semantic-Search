from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import SubTopic, VideoContent

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    session = SessionLocal()
    try:
        # Check if data already exists
        existing_subtopics = session.query(SubTopic).count()
        if existing_subtopics > 0:
            print("Data already exists. Skipping seed.")
            return

        # Sample Data
        subtopics_data = [
            {"id": 1, "text": "Introduction to Python Programming"},
            {"id": 2, "text": "Data Structures in Python"},
            {"id": 3, "text": "Object-Oriented Programming (OOP) Concepts"},
            {"id": 4, "text": "Web Development with Flask and Django"},
            {"id": 5, "text": "Machine Learning Basics with Scikit-Learn"},
            {"id": 6, "text": "Deep Learning with TensorFlow and Keras"},
            {"id": 7, "text": "Natural Language Processing (NLP) Fundamentals"},
            {"id": 8, "text": "Computer Vision Techniques"},
            {"id": 9, "text": "Database Management with SQL"},
            {"id": 10, "text": "Cloud Computing with AWS and Azure"}
        ]

        # Insert SubTopics
        for item in subtopics_data:
            subtopic = SubTopic(SubTopicID=item["id"], SubTopic=item["text"])
            session.add(subtopic)
        
        session.commit()
        print(f"Inserted {len(subtopics_data)} subtopics.")

        # Sample Videos
        videos_data = [
            {"id": 1, "sub_id": 1, "caption": "Setting up Python Environment", "file": "python_setup.mp4", "thumb": "python_setup.jpg"},
            {"id": 2, "sub_id": 1, "caption": "Variables and Data Types", "file": "vars_types.mp4", "thumb": "vars_types.jpg"},
            {"id": 3, "sub_id": 2, "caption": "Lists, Tuples, and Dictionaries", "file": "data_structs.mp4", "thumb": "data_structs.jpg"},
            {"id": 4, "sub_id": 3, "caption": "Classes and Objects", "file": "classes_objects.mp4", "thumb": "classes_objects.jpg"},
            {"id": 5, "sub_id": 5, "caption": "Linear Regression Explained", "file": "linear_reg.mp4", "thumb": "linear_reg.jpg"},
            {"id": 6, "sub_id": 6, "caption": "Neural Networks Introduction", "file": "neural_nets.mp4", "thumb": "neural_nets.jpg"},
            {"id": 7, "sub_id": 9, "caption": "SQL Select Statements", "file": "sql_select.mp4", "thumb": "sql_select.jpg"},
            {"id": 8, "sub_id": 10, "caption": "Deploying on Azure App Service", "file": "azure_deploy.mp4", "thumb": "azure_deploy.jpg"}
        ]

        # Insert Videos
        for item in videos_data:
            video = VideoContent(
                VCId=item["id"],
                SubTopicID=item["sub_id"],
                VideoCaption=item["caption"],
                VideoFileName=item["file"],
                Thumbnail=item["thumb"]
            )
            session.add(video)

        session.commit()
        print(f"Inserted {len(videos_data)} videos.")

    except Exception as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
