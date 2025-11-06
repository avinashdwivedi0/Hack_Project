import asyncio
from bson import ObjectId
from app.database import skill_tracks_col, quizzes_col, progress_col

async def seed():
    print("Seeding Roadmaps + Quizzes...")

    await skill_tracks_col.delete_many({})
    await quizzes_col.delete_many({})
    await progress_col.delete_many({})

    roadmaps = [
        ("Web Development", [
            (1, ["HTML Basics", "Tags", "Page Structure"], ["https://youtu.be/qz0aGYrrlhU"]),
            (2, ["CSS Basics", "Selectors", "Flexbox"], ["https://youtu.be/1Rs2ND1ryYc"]),
            (3, ["Responsive Design", "Media Queries"], ["https://youtu.be/srvUrASNj0s"]),
        ]),
        ("DSA in Java", [
            (1, ["Arrays", "Loops", "Basic Patterns"], ["https://youtu.be/8lwO0Zy-L1Q"]),
            (2, ["Functions", "Recursion"], ["https://youtu.be/jEC8HZ3x0kE"]),
            (3, ["Sorting: Bubble, Selection, Insertion"], ["https://youtu.be/lyZQPjUT5B4"]),
        ]),
        ("Data Science", [
            (1, ["Python Basics", "NumPy"], ["https://youtu.be/QUT1VHiLmmI"]),
            (2, ["Pandas", "DataFrames"], ["https://youtu.be/vmEHCJofslg"]),
            (3, ["Matplotlib", "Visualization"], ["https://youtu.be/3Xc3CA655Y4"]),
        ]),
    ]

    # insert skill tracks and map names -> ids
    name_to_id = {}
    for name, weeks in roadmaps:
        for week_number, topics, links in weeks:
            res = await skill_tracks_col.insert_one({
                "skill_name": name,
                "week_number": week_number,
                "topics": topics,
                "video_links": links
            })
        # fetch first doc to get id
        doc = await skill_tracks_col.find_one({"skill_name": name})
        name_to_id[name] = str(doc["_id"])

    # starter quizzes (2 each) – now with skill_id
    starters = [
        ("Web Development", "What does HTML stand for?",
         ["Hyper Trainer Marking Language", "Hyper Text Markup Language", "High Text Machine Language", "Hyperloop Transfer Markup Language"], 1),
        ("Web Development", "Which tag is used for headings?",
         ["<p>", "<h1>", "<title>", "<head>"], 1),

        ("DSA in Java", "Time complexity of binary search is:",
         ["O(n)", "O(n^2)", "O(log n)", "O(1)"], 2),
        ("DSA in Java", "Which data structure works on FIFO?",
         ["Stack", "Queue", "Tree", "Graph"], 1),

        ("Data Science", "Which library is used for dataframes?",
         ["NumPy", "Pandas", "Matplotlib", "SciPy"], 1),
        ("Data Science", "Which library is used for visualization?",
         ["NumPy", "Pandas", "Matplotlib", "TensorFlow"], 2),
    ]

    bulk = []
    for skill_name, q, opts, ans_idx in starters:
        bulk.append({
            "skill_id": name_to_id[skill_name],
            "skill_name": skill_name,
            "question": q,
            "options": opts,
            "correct_answer": ans_idx
        })
    if bulk:
        await quizzes_col.insert_many(bulk)

    print("✅ Seeding Completed!")

if __name__ == "__main__":
    asyncio.run(seed())
