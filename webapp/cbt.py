questions = [
    {
        'course_id': 1,
        'question_text': "Low annual rainfall, sparse vegetation, high diurnal temperatures and cold nights are characteristic features of the",
        'option_a': "tropical rainforest",
        'option_b': "desert",
        'option_c': "montane forest",
        'option_d': "guinea savanna",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "The activity of an organism which affects the survival of another organism in the same habitat constitutes",
        'option_a': "an edaphic factor",
        'option_b': "an abiotic factor",
        'option_c': "a biotic factor",
        'option_d': "a physiographic factor",
        'correct_option': "C",
    },
    {
        'course_id': 1,
        'question_text': "The average number of individuals of a species per unit area of the habitat is the",
        'option_a': "population density",
        'option_b': "population frequency",
        'option_c': "population size",
        'option_d': "population distribution",
        'correct_option': "A",
    },
    {
        'course_id': 1,
        'question_text': "The vector for yellow fever is",
        'option_a': "Aedes mosquito",
        'option_b': "Anopheles mosquito",
        'option_c': "tsetse fly",
        'option_d': "blackfly",
        'correct_option': "A",
    },
    {
        'course_id': 1,
        'question_text': "The loss of soil through erosion can be reduced by",
        'option_a': "watering",
        'option_b': "crop rotation",
        'option_c': "manuring",
        'option_d': "irrigation",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "The protozoan plasmodium falciparum is transmitted by",
        'option_a': "female Anopheles mosquitoes",
        'option_b': "female Aedes mosquitoes",
        'option_c': "female Culex mosquitoes",
        'option_d': "Female blackfly",
        'correct_option': "A",
    },
    {
        'course_id': 1,
        'question_text': "Which of the following is most advanced in the evolutionary trend of animals?",
        'option_a': "Liver fluke",
        'option_b': "Earthworm",
        'option_c': "Snail",
        'option_d': "Cockroach",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "Which of the following is the lowest category of classification?",
        'option_a': "Class",
        'option_b': "Species",
        'option_c': "Family",
        'option_d': "Order",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "Plants that show secondary growth are usually found among the",
        'option_a': "thallophytes",
        'option_b': "pteridophytes",
        'option_c': "monocotyledons",
        'option_d': "dicotyledons",
        'correct_option': "D",
    },
    {
        'course_id': 1,
        'question_text': "The fungi are distinct group of eukaryotes mainly because they have",
        'option_a': "spores",
        'option_b': "no chlorophyll",
        'option_c': "many fruiting bodies",
        'option_d': "sexual and sexual reproduction",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "An arthropod that is destructive at early stage of its life cycle is",
        'option_a': "butterfly",
        'option_b': "mosquito",
        'option_c': "bee",
        'option_d': "millipede",
        'correct_option': "A",
    },
    {
        'course_id': 1,
        'question_text': "An animal body that can be cut along its axis in any plane to give two identical parts is said to be",
        'option_a': "radially symmetrical",
        'option_b': "bilaterally symmetrical",
        'option_c': "asymmetrical",
        'option_d': "symmetrical",
        'correct_option': "A",
    },
    {
        'course_id': 1,
        'question_text': "Which of the following possesses mammary gland?",
        'option_a': "Dogfish",
        'option_b': "whale",
        'option_c': "shark",
        'option_d': "catfish",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "The feature that links birds to reptiles in evolution is the possession of",
        'option_a': "feathers",
        'option_b': "break",
        'option_c': "skeleton",
        'option_d': "scales",
        'correct_option': "D",
    },
    {
        'course_id': 1,
        'question_text': "The process in which complex substances are broken down into simpler ones is referred to as",
        'option_a': "anabolism",
        'option_b': "catabolism",
        'option_c': "metabolism",
        'option_d': "tropism",
        'correct_option': "B",
    },
    {
        'course_id': 1,
        'question_text': "The organ which is sensitive to light in Euglena is the",
        'option_a': "gullet",
        'option_b': "flagellum",
        'option_c': "chloroplast",
        'option_d': "eyespot",
        'correct_option': "D",
    },
    {
        'course_id': 1,
        'question_text': "The organelles present in cells that are actively respiring and photosynthesizing are",
        'option_a': "lysosomes and ribosomes",
        'option_b': "Golgi apparatus and endoplasmic reticulum",
        'option_c': "nucleus and centrioles",
        'option_d': "mitochondria and chloroplast",
        'correct_option': "D",
    },
    {
        'course_id': 1,
        'question_text': "Taenia solium can be found in",
        'option_a': "cow",
        'option_b': "goat",
        'option_c': "dog",
        'option_d': "pig",
        'correct_option': "D",
    },
    {
        'course_id': 1,
        'question_text': "The structure labelled II is the",
        'option_a': "spermathecal pore",
        'option_b': "cocoon",
        'option_c': "clitellum",
        'option_d': "chaetae",
        'correct_option': "C",
    },
]




# questions = [
#      {
#         'course_id': 1,
#         'question_text': "",
#         'option_a': "",
#         'option_b': "",
#         'option_c': "",
#         'option_d': "",
#         'correct_option': "",
#     },
# ]


# from webapp.cbt import questions
# from webapp.models import Course, PastQuestionsObj

# for question_data in questions:
#     try:
#         course = Course.objects.get(id=question_data['course_id'])
#         PastQuestionsObj.objects.create(
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
