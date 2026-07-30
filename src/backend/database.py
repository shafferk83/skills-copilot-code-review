"""
MongoDB database configuration and setup for Mergington High School API
"""

from pymongo import MongoClient
from argon2 import PasswordHasher, exceptions as argon2_exceptions

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mergington_high']
activities_collection = db['activities']
teachers_collection = db['teachers']
internships_collection = db['internships']
tasks_collection = db['tasks']

# Methods


def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """Verify a plain password against an Argon2 hashed password.

    Returns True when the password matches, False otherwise.
    """
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except argon2_exceptions.VerifyMismatchError:
        return False
    except Exception:
        # For any other exception (e.g., invalid hash), treat as non-match
        return False


def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})

    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one(
                {"_id": teacher["username"], **teacher})

    # Initialize internships if empty
    if internships_collection.count_documents({}) == 0:
        for internship in initial_internships:
            internships_collection.insert_one(internship)


# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
    },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

initial_internships = [
    {
        "company": "TechNova Solutions",
        "role": "Software Engineering Intern",
        "location": "San Francisco, CA (Remote)",
        "branch": "Technology",
        "prerequisites": "Python or Java basics, interest in software development",
        "link": "https://technova.example.com/internships"
    },
    {
        "company": "BioLife Labs",
        "role": "Research Intern",
        "location": "Boston, MA",
        "branch": "Science",
        "prerequisites": "Biology or Chemistry coursework, lab safety training",
        "link": "https://biolabs.example.com/careers"
    },
    {
        "company": "Meridian Media",
        "role": "Graphic Design Intern",
        "location": "New York, NY (Hybrid)",
        "branch": "Arts",
        "prerequisites": "Portfolio of artwork, familiarity with design tools",
        "link": "https://meridianmedia.example.com/internships"
    },
    {
        "company": "Summit Finance Group",
        "role": "Finance & Analytics Intern",
        "location": "Chicago, IL",
        "branch": "Business",
        "prerequisites": "Math coursework, interest in finance",
        "link": "https://summitfinance.example.com/internships"
    },
    {
        "company": "GreenEarth Initiative",
        "role": "Environmental Science Intern",
        "location": "Portland, OR (Remote)",
        "branch": "Science",
        "prerequisites": "Environmental science or biology coursework",
        "link": "https://greenearth.example.com/internships"
    },
    {
        "company": "CivicBridge",
        "role": "Community Outreach Intern",
        "location": "Washington, D.C.",
        "branch": "Social Studies",
        "prerequisites": "Strong communication skills, interest in public service",
        "link": "https://civicbridge.example.com/internships"
    },
    {
        "company": "PixelForge Games",
        "role": "Game Development Intern",
        "location": "Austin, TX (Hybrid)",
        "branch": "Technology",
        "prerequisites": "Programming basics, interest in game design",
        "link": "https://pixelforge.example.com/internships"
    },
    {
        "company": "Harmony Health",
        "role": "Healthcare Administration Intern",
        "location": "Houston, TX",
        "branch": "Health",
        "prerequisites": "Interest in healthcare, strong organizational skills",
        "link": "https://harmonyhealth.example.com/careers"
    },
    {
        "company": "EduPath Learning",
        "role": "Education Technology Intern",
        "location": "Remote",
        "branch": "Education",
        "prerequisites": "Interest in education, familiarity with digital tools",
        "link": "https://edupathlearning.example.com/internships"
    },
    {
        "company": "Apex Engineering",
        "role": "Mechanical Engineering Intern",
        "location": "Detroit, MI",
        "branch": "Engineering",
        "prerequisites": "Physics and math coursework, interest in engineering",
        "link": "https://apexengineering.example.com/internships"
    }
]
