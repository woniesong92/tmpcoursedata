import pdb
import json
import sys
import os
from pymongo import MongoClient
  

# def main(args):
  # ADDS ALL CS COURSES
  # single file version

  # client = MongoClient('mongodb://127.0.0.1:3001/meteor')
  # courses = client.meteor.courses

  # args = args[1:]

  # for file_name in args:
  #   with open(file_name, 'r') as f:
  #     parsed_data = json.load(f)
  #     classes = parsed_data["data"]["classes"]
  #     for class_data in classes:
  #       _classNbrs = []
  #       for class_section in class_data["enrollGroups"][0]["classSections"]:
  #         _classNbrs.append(class_section["classNbr"])

  #       meetings = class_data["enrollGroups"][0]["classSections"][0]["meetings"]
        # unitsMin = class_data["enrollGroups"][0]["unitsMinimum"]
        # unitsMax = class_data["enrollGroups"][0]["unitsMaximum"]

  #       if (meetings):
  #         instructors = meetings[0]["instructors"]
  #         if (instructors):
  #           instructor = " ".join([instructors[0]["firstName"], instructors[0]["lastName"]])
  #         else:
  #           instructor = "n/a"

  #       course = {
  #         "subject": class_data["subject"],
  #         "catalogNbr": class_data["catalogNbr"],
  #         "catalog": class_data["subject"]+str(class_data["catalogNbr"]),
  #         "titleLong": class_data["titleLong"],
  #         "titleShort": class_data["titleShort"],
  #         "instructor": instructor,
  #         "catalogWhenOffered": class_data["catalogWhenOffered"],
  #         "description": class_data["description"],
  #         "crseId": class_data["crseId"],
  #         "classNbrs": ",".join([str(x) for x in _classNbrs]),
            # "unitsMin": unitsMin,
            # "unitsMax": unitsMax,
  #         "votes": 0,
  #         "upvoters": []
  #       }

  #       courses.insert(course)

def main(args):
  # client = MongoClient('mongodb://127.0.0.1:3001/meteor')
  # courses = client.meteor.courses

  client = MongoClient('mongodb://localhost/CornellCourseReview')
  courses = client.CornellCourseReview.courses

  # file_names = [x for x in os.listdir('.') if x.endswith('json')]
  file_names = [x for x in os.listdir(args[1]) if x.startswith('classes.json')]

  for file_name in file_names:
    print "processing", file_name
    with open(file_name, 'r') as f:
      # courses_to_add = {}

      parsed_data = json.load(f)
      classes = parsed_data["data"]["classes"]
      for class_data in classes:
        _classNbrs = []
        for class_section in class_data["enrollGroups"][0]["classSections"]:
          _classNbrs.append(class_section["classNbr"])

        meetings = class_data["enrollGroups"][0]["classSections"][0]["meetings"]
        unitsMin = class_data["enrollGroups"][0]["unitsMinimum"]
        unitsMax = class_data["enrollGroups"][0]["unitsMaximum"]

        if (meetings):
          instructors = meetings[0]["instructors"]
          if (instructors):
            instructor = " ".join([instructors[0]["firstName"], instructors[0]["lastName"]])
          else:
            instructor = "n/a"

        catalog = class_data["subject"]+str(class_data["catalogNbr"])

        # SKIP IF the course already exists
        existing_course = courses.find_one({"catalog": catalog})
        if existing_course:
          continue
          # cur_instructor = existing_course['instructor']
          # if (instructor != 'n/a') and (not instructor in cur_instructor):
          #   cur_instructor.append(instructor)
          #   courses.update({'_id':existing_course['_id']}, {'$set':{'instructor': cur_instructor}},upsert=False, multi=False)
          #   print catalog, "More instructos:", cur_instructor
        else:
          course = {
            "subject": class_data["subject"],
            "catalogNbr": class_data["catalogNbr"],
            "catalog": catalog,
            "titleLong": class_data["titleLong"],
            "titleShort": class_data["titleShort"],
            "instructor": [instructor],
            "catalogWhenOffered": class_data["catalogWhenOffered"],
            "description": class_data["description"],
            # "crseId": class_data["crseId"],
            # "classNbrs": ",".join([str(x) for x in _classNbrs]),
            "unitsMin": unitsMin,
            "unitsMax": unitsMax,
            "votes": 0,
            "upvoters": []
          }

          courses.insert(course)
          print "Added", catalog

if __name__ == "__main__":
  main(sys.argv)
