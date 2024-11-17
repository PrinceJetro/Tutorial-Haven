from .models import Course, CBTQuestion

questions = [
    {
        'course_id': 3,
        'question_text': "What is the primary purpose of a spectrophotometer in an experiment?",
        'option_a': "To measure the absorbance of a solution",
        'option_b': "To analyze the structure of an atom",
        'option_c': "To identify microbial species",
        'option_d': "To measure electrical conductivity",
        'correct_option': "A"
    },
    {
        'course_id': 3,
        'question_text': "Which element in Group 1 is most reactive?",
        'option_a': "Sodium",
        'option_b': "Lithium",
        'option_c': "Potassium",
        'option_d': "Cesium",
        'correct_option': "D"
    },
    {
        'course_id': 3,
        'question_text': "In research methodology, the purpose of the 'Materials and Methods' section is to:",
        'option_a': "Summarize the findings of the study",
        'option_b': "Explain the procedure and tools used in the study",
        'option_c': "Provide background information on the topic",
        'option_d': "List the sources and references used",
        'correct_option': "B"
    },
    {
        'course_id': 3,
        'question_text': "Flame photometry is primarily used to measure the concentration of which type of elements?",
        'option_a': "Noble gases",
        'option_b': "Metals",
        'option_c': "Nonmetals",
        'option_d': "Metalloids",
        'correct_option': "B"
    },
    {
        'course_id': 3,
        'question_text': "What is the main focus of a literature review in research?",
        'option_a': "To present new experimental results",
        'option_b': "To summarize previous studies on the topic",
        'option_c': "To outline the research budget",
        'option_d': "To explain the study’s limitations",
        'correct_option': "B"
    },
    {
        'course_id': 3,
        'question_text': "In microbiology, which type of media is best for growing non-fastidious bacteria?",
        'option_a': "Selective media",
        'option_b': "Differential media",
        'option_c': "Complex media",
        'option_d': "Synthetic media",
        'correct_option': "C"
    },
    {
        'course_id': 3,
        'question_text': "During the preparation of culture media in a lab, sterilization is essential to:",
        'option_a': "Enhance microbial growth",
        'option_b': "Prevent contamination",
        'option_c': "Increase nutrient concentration",
        'option_d': "Reduce humidity",
        'correct_option': "B"
    },
    {
        'course_id': 3,
        'question_text': "Which Group 2 element is used in fireworks for its distinctive red flame?",
        'option_a': "Calcium",
        'option_b': "Magnesium",
        'option_c': "Strontium",
        'option_d': "Barium",
        'correct_option': "C"
    },
    {
        'course_id': 3,
        'question_text': "Which referencing style is commonly used in the social sciences?",
        'option_a': "APA",
        'option_b': "Chicago",
        'option_c': "IEEE",
        'option_d': "MLA",
        'correct_option': "A"
    },
    {
        'course_id': 3,
        'question_text': "In atomic spectroscopy, the energy of emitted photons is directly related to:",
        'option_a': "The type of detector used",
        'option_b': "The difference in energy levels of an atom",
        'option_c': "The wavelength of incident light",
        'option_d': "The amount of sample used",
        'correct_option': "B"
    }
]


# from webapp.cbt import questions
# from webapp.models import Course, CBTQuestion
# from webapp.cbt import questions  # Adjust this import based on the actual location of `cbt.py`

# for question_data in questions:
#     try:
#         course = Course.objects.get(id=question_data['course_id'])
#         CBTQuestion.objects.create(
#             course=course,
#             question_text=question_data['question_text'],
#             option_a=question_data['option_a'],
#             option_b=question_data['option_b'],
#             option_c=question_data['option_c'],
#             option_d=question_data['option_d'],
#             correct_option=question_data['correct_option']
#         )
#         print(f"Added question: {question_data['question_text']}")
#     except Course.DoesNotExist:
#         print(f"Course with ID {question_data['course_id']} does not exist.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
