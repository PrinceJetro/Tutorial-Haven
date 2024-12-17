# questions =



# questions = [
#      {
#         'course_id': 10,
#         'question_text': "",
#         'option_a': "",
#         'option_b': "",
#         'option_c': "",
#         'option_d': "",
#         'correct_option': "",
#     },
# ]


from webapp.cbt import questions
from webapp.models import Course, PastQuestionsObj, Topic

for question_data in questions:
    try:
        course = Course.objects.get(id=question_data['course_id'])
        PastQuestionsObj.objects.create(
            course=course,
            question_text=question_data['question_text'],
            option_a=question_data['option_a'],
            option_b=question_data['option_b'],
            option_c=question_data['option_c'],
            option_d=question_data['option_d'],
            correct_option=question_data['correct_option']
        )
        print(f"Added question: {course} {question_data['question_text']}")
    except Course.DoesNotExist:
        print(f"Course with ID {question_data['course_id']} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")























# from webapp.cbt import questions
# from webapp.models import Course, Topic

# for question_data in questions:
#     try:
#         course = Course.objects.get(id=question_data['course_id'])
#         Topic.objects.create(
#             course=course,
#             content=question_data['content'],
#             name=question_data['name']
#         )
#         print(f"Added question: {question_data['name']}")
#     except Course.DoesNotExist:
#         print(f"Course with ID {question_data['course_id']} does not exist.")
#     except Exception as e:
#         print(f"An error occurred: {e}")