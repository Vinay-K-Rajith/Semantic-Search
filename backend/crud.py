from sqlalchemy import select
from sqlalchemy.orm import Session
from models import SubTopic, VideoContent
from database import SessionLocal

def fetch_all_subtopics():
    session = SessionLocal()
    try:
        # Fetch all subtopics
        stmt = select(SubTopic.SubTopicID, SubTopic.SubTopic)
        results = session.execute(stmt).all()
        return [{'id': r[0], 'text': r[1]} for r in results]
    except Exception as e:
        print(f'[ERROR] fetch_all_subtopics: {e}')
        return []
    finally:
        session.close()

def fetch_videos_for_subtopics(subtopic_ids):
    if not subtopic_ids:
        return []
        
    session = SessionLocal()
    try:
        # Fetch videos where SubTopicID is in the list
        stmt = select(VideoContent).where(VideoContent.SubTopicID.in_(subtopic_ids))
        results = session.execute(stmt).scalars().all()
        
        # Format as list of dicts: {'vc_id': ..., 'subtopic_id': ..., 'caption': ..., 'file_name': ..., 'thumbnail': ...}
        return [
            {
                'vc_id': v.VCId,
                'subtopic_id': v.SubTopicID,
                'caption': v.VideoCaption,
                'file_name': v.VideoFileName,
                'thumbnail': v.Thumbnail
            }
            for v in results
        ]
    except Exception as e:
        print(f'[ERROR] fetch_videos_for_subtopics: {e}')
        return []
    finally:
        session.close()
