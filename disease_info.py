
DISEASE_INFO = {
    "Grape Black Measles": {
        "common_name": "Black Measles (Esca)",
        "overview": (
            "A grapevine disease associated with a complex of fungi that "
            "affect the woody parts of the vine. A model prediction alone "
            "cannot confirm Esca."
        ),
        "symptoms": [
            "Yellow or reddish stripes between leaf veins",
            "Leaf tissue may dry out or become brown",
            "Small dark spots with brown-purple borders may appear on berries",
            "Affected leaves may dry and fall prematurely",
        ],
        "prevention": [
            "Inspect vines regularly for unusual leaf and wood symptoms.",
            "Prune affected wood using appropriate vineyard sanitation practices.",
            "Remove infected pruning material from the vineyard.",
            "Seek advice from a grape disease specialist about affected vines.",
        ],
        "treatment_note": (
            "Trunk diseases can be difficult to manage. No chemical treatment "
            "is prescribed here. Ask a qualified local grape specialist to "
            "confirm the disease and recommend suitable management."
        ),
        "sources": [
            {
                "title": "UC IPM: Esca (Black Measles)",
                "url": "https://ipm.ucanr.edu/agriculture/grape/esca-black-measles/",
            },
        ],
    },

    "Grape Black rot": {
        "common_name": "Grape Black Rot",
        "overview": (
            "A fungal disease that can affect grape leaves, shoots and fruit. "
            "Infected berries may shrivel and become hard, dark mummies."
        ),
        "symptoms": [
            "Small brown leaf spots with darker margins",
            "Dark fungal structures may appear within spots",
            "Infected berries may turn dark, shrivel and dry out",
            "Dark lesions may develop on shoots and tendrils",
        ],
        "prevention": [
            "Remove mummified berries and infected plant material.",
            "Keep the vineyard free of leftover diseased fruit.",
            "Inspect leaves, shoots and fruit regularly, especially after rain.",
            "Maintain suitable canopy airflow and avoid unnecessary leaf wetness.",
        ],
        "treatment_note": (
            "Management depends on disease confirmation, crop stage and local "
            "conditions. Consult a qualified agricultural officer before "
            "choosing a fungicide."
        ),
        "sources": [
            {
                "title": "Penn State Extension: Grape Black Rot",
                "url": "https://extension.psu.edu/grape-disease-black-rot",
            },
            {
                "title": "Agriculture and Agri-Food Canada: Grape Disease Guide",
                "url": (
                    "https://agriculture.canada.ca/en/agricultural-production/"
                    "crop-protection/agricultural-pest-management-resources/"
                    "identification-guide-major-diseases-grapes"
                ),
            },
        ],
    },

    "Grape Healthy": {
        "common_name": "Healthy-Looking Grape Leaf",
        "overview": (
            "The model did not identify one of the three supported diseases "
            "in this image. This does not prove that the vine is completely "
            "healthy or rule out other diseases, pests or nutrient problems."
        ),
        "symptoms": [
            "No supported disease was selected by the model.",
            "Check the whole vine for spots, discoloration, wilting or damage.",
        ],
        "prevention": [
            "Inspect vines regularly for changes in leaves, shoots and fruit.",
            "Maintain balanced irrigation and appropriate vineyard nutrition.",
            "Keep tools clean and follow good vineyard sanitation practices.",
        ],
        "treatment_note": (
            "No disease treatment is suggested from this prediction alone. "
            "Investigate any visible symptoms with a qualified specialist."
        ),
        "sources": [
            {
                "title": "UC IPM: Grape Pest Management Guidelines",
                "url": "https://ipm.ucanr.edu/agriculture/grape/",
            },
        ],
    },

    "Grape Isariopsis Leaf Spot": {
        "common_name": "Grape Isariopsis Leaf Spot",
        "overview": (
            "A leaf-spot disease category in the model. Similar-looking leaf "
            "spots can have different causes, so the prediction needs "
            "confirmation before disease-specific treatment."
        ),
        "symptoms": [
            "Leaf spots or patches may be visible.",
            "Spot colour, shape and distribution should be examined closely.",
            "Other diseases or non-infectious problems may look similar.",
        ],
        "prevention": [
            "Inspect both sides of leaves and monitor how spots develop.",
            "Remove heavily affected fallen plant material where appropriate.",
            "Avoid unnecessary prolonged leaf wetness.",
            "Get an expert diagnosis if symptoms spread or worsen.",
        ],
        "treatment_note": (
            "Disease-specific treatment has not been verified here. Do not "
            "select a fungicide based only on the model label; confirm the "
            "causal disease and obtain locally approved guidance."
        ),
        "sources": [
            {
                "title": "TNAU Agritech Portal: Grape Disease Information",
                "url": (
                    "https://agritech.tnau.ac.in/crop_protection/"
                    "crop_prot_postharvest_grapes_1.html"
                ),
            },
            {
                "title": "UC IPM: Grape Disease Management",
                "url": "https://ipm.ucanr.edu/agriculture/grape/",
            },
        ],
    },
}


def get_disease_info(predicted_class):
    """Return disease information for a supported model class."""
    return DISEASE_INFO.get(predicted_class)
