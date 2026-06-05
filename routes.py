from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os

from models import db, StandupPost

standup_bp = Blueprint("standup_bp", __name__)

UPLOAD_FOLDER = "uploads"


# GET ALL STANDUPS
@standup_bp.route("/standups/", methods=["GET"])
def get_standups():

    standups = StandupPost.query.order_by(
        StandupPost.timestamp.desc()
    ).all()

    return jsonify([post.to_dict() for post in standups])


# CREATE STANDUP
@standup_bp.route("/standups/", methods=["POST"])
def create_standup():

    author = request.form.get("author")
    yesterday = request.form.get("yesterday")
    today = request.form.get("today")
    blockers = request.form.get("blockers")
    has_blocker = request.form.get("has_blocker") == "true"

    # VALIDATION
    if not author or not yesterday or not today:

        return jsonify({
            "error": "Author, yesterday and today are required"
        }), 400

    filename = None

    file = request.files.get("file")

    # HANDLE FILE UPLOAD
    if file:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(file.filename)

        file.save(os.path.join(UPLOAD_FOLDER, filename))

    # CREATE NEW POST
    new_post = StandupPost(
        author=author,
        yesterday=yesterday,
        today=today,
        blockers=blockers,
        has_blocker=has_blocker,
        file_attachment=filename,
        timestamp=datetime.utcnow() + timedelta(hours=3)
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

# DELETE STANDUP
@standup_bp.route("/standups/<int:id>", methods=["DELETE"])
def delete_standup(id):
   post = StandupPost.query.get(id)
  
   if not post:
       return jsonify({"error": "Standup not found"}), 404
  
   # Delete the file if it exists
   if post.file_attachment:
       file_path = os.path.join(UPLOAD_FOLDER, post.file_attachment)
       if os.path.exists(file_path):
           os.remove(file_path)
  
   db.session.delete(post)
   db.session.commit()
  
   return jsonify({"message": "Standup deleted successfully"}), 200

# DASHBOARD STATS
@standup_bp.route("/standups/stats/", methods=["GET"])
def get_stats():

    posts_per_day = []

    blocker_count = 0

    for i in range(6, -1, -1):

        day = datetime.utcnow().date() - timedelta(days=i)

        count = StandupPost.query.filter(
            db.func.date(StandupPost.timestamp) == day
        ).count()

        blockers = StandupPost.query.filter(
            db.func.date(StandupPost.timestamp) == day,
            StandupPost.has_blocker == True
        ).count()

        blocker_count += blockers

        posts_per_day.append({
            "date": day.strftime("%Y-%m-%d"),
            "count": count,
            "blockers": blockers
        })

    return jsonify({
        "posts_per_day": posts_per_day,
        "blocker_count": blocker_count
    })