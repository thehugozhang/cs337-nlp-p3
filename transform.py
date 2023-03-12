from recipe_scrapers import scrape_me
from ingredient_parser import parse_multiple_ingredients, parse_ingredient
import pprint

scraper = scrape_me("https://www.allrecipes.com/recipe/285077/easy-one-pot-ground-turkey-pasta/")

# Original value recipe values.
original_recipe_prep_time = scraper.total_time()
# unprocessed_ingredients = scraper.ingredients()
# original_recipe_ingredients = [x.lower() for x in unprocessed_ingredients]
original_recipe_ingredients = scraper.ingredients()
original_recipe_parsed_ingredients = parse_multiple_ingredients(original_recipe_ingredients)
original_recipe_instructions = scraper.instructions_list()


# Updated value recipe values.
updated_recipe_prep_time = original_recipe_prep_time
updated_recipe_ingredients = original_recipe_ingredients.copy()
updated_recipe_parsed_ingredients = sorted(original_recipe_parsed_ingredients.copy(), key=lambda d: d['name'])
updated_recipe_instructions = original_recipe_instructions.copy()

print(updated_recipe_parsed_ingredients)
meat_products = ["beef", "chicken", "pork", "lamb", "goat", "turkey", "veal", "duck", "goose", "rabbit", "sausage", "hot dog", "bratwurst", "cow", "pig", "liver", "tripe", "offal", "gelatin"]

meat_substitutions = {
    "beef stock": { "substitution": "vegetable stock", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "beef broth": { "substitution": "vegetable broth", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "ground beef": { "substitution": "brown lentils", "ratio": 1.0, "unit": "cup", "sentence": " cup(s) of dried, uncooked brown lentils", "comment": "dried, uncooked", "additions": { "prep_time": 15, "ingredients": ["3 cups water"], "steps": ["Place the lentils and water in a large saucepan.", "Bring to a rapid simmer, then reduce the heat and simmer for about 15 minutes until the lentils are tender but still hold their shape. Drain any excess liquid and set aside for later use."] }},
    "beef": { "substitution": "tempeh", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken stock": { "substitution": "vegetable stock", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken broth": { "substitution": "vegetable broth", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken breast": { "substitution": "seitan slice", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken thigh": { "substitution": "seitan slice", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken wing": { "substitution": "seitan slice", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken leg": { "substitution": "seitan slice", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "chicken": { "substitution": "seitan", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "pork bones": { "substitution": "vegetable scraps", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "pork": { "substitution": "jackfruit", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "lamb": { "substitution": "eggplant", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "goat": { "substitution": "tempeh", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "turkey": { "substitution": "tofurky", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "veal": { "substitution": "beets", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "bone broth": { "substitution": "vegetable broth", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "bones": { "substitution": "vegetable scraps", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
}

seafood_substitutions = {
    "lobster": { "substitution": "vegan lobster", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "crab": { "substitution": "vegan crab", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "shrimp": { "substitution": "vegan shrimp", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
    "fish": { "substitution": "vegan fish", "ratio": 1.0, "unit": None, "sentence": None, "comment": None, "additions": { "prep_time": 0, "ingredients": [], "steps": []} },
}

vegetable_substitutions = {

}

healthy_substitutions = {

}

unhealthy_substitutions = {
    
}


def construct_substitute_ingredient(previous, meat_product, substitute_dict, recipe_time, recipe_ingredients, recipe_steps, original_recipe_steps):
    """Converts an ingredient with its substitute and adjusts the recipe using its parameters."""
    # Shallow copies to prevent changing after assignment.
    shallow_recipe_time = recipe_time
    shallow_recipe_ingredients = recipe_ingredients
    shallow_recipe_steps = recipe_steps

    # Get substitute values for current ingredient.
    substitute_type = substitute_dict["substitution"]
    substitute_ratio = substitute_dict["ratio"]
    substitute_unit = substitute_dict["unit"]
    substitute_sentence = substitute_dict["sentence"]
    substitute_comment = substitute_dict["comment"]
    # Get additional prep time, ingredients, and steps for substitution (if any).
    substitute_added_time = substitute_dict["additions"]["prep_time"]
    substitute_added_ingredients = substitute_dict["additions"]["ingredients"]
    substitute_added_steps = substitute_dict["additions"]["steps"]

    # Update current ingredient name.
    previous["name"] = previous["name"].lower().replace(meat_product, substitute_type)

    # Adjust original ingredient quantity using substitute ratio and unit.
    previous["quantity"] = "{:.2f}".format((float(previous["quantity"]) * substitute_ratio))
    if substitute_unit is not None:
        previous["unit"] = substitute_unit

    # Update original ingredient dictionary using substitute values.
    if substitute_sentence is not None:
        previous["sentence"] = previous["quantity"] + substitute_sentence
    if substitute_comment is not None:
        previous["comment"] = substitute_comment
    else:
        previous["sentence"] = previous["sentence"].lower().replace(meat_product, substitute_type).capitalize()

    # Add additional prep time to recipe.
    shallow_recipe_time += substitute_added_time


    # Add additional steps to recipe.
    shallow_recipe_steps = substitute_added_steps + shallow_recipe_steps

    # Parse new ingredients and add to ingredient list.
    for new_ingredient in substitute_added_ingredients:
        shallow_recipe_ingredients.append(parse_ingredient(new_ingredient))

    return shallow_recipe_time, shallow_recipe_ingredients, shallow_recipe_steps

pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(parsed_ingredients)

for ingredient_dict in original_recipe_parsed_ingredients:
    for meat_product, substitute_dict in meat_substitutions.items():
        if meat_product in ingredient_dict["name"].lower():
            updated_recipe_prep_time, updated_recipe_parsed_ingredients, updated_recipe_instructions = construct_substitute_ingredient(ingredient_dict, meat_product, substitute_dict, updated_recipe_prep_time, updated_recipe_parsed_ingredients, updated_recipe_instructions, original_recipe_instructions)
            print("need to substitute:", ingredient_dict["name"])
            break


    # # Update all steps in recipe to replace references of meat products with substitute.
    # # Must use original steps here to prevent from indexing overwritten steps.
    # # Ex. "chicken" will overwrite "chicken broth" to "seitan broth".
    # for index, step in enumerate(original_recipe_steps):
    #     step = step.lower()
    #     if meat_product in step:
    #         temp_step = step.replace(meat_product, substitute_type).capitalize()
    #         shallow_recipe_steps[index] = '. '.join(sentence.capitalize() for sentence in temp_step.split('. '))

# Final check through for any remaining references.
for meat_product, substitute_dict in meat_substitutions.items():
    for index, step in enumerate(updated_recipe_instructions):
        step = step.lower()
        if meat_product in step:
            temp_step = step.replace(meat_product, substitute_dict["substitution"]).capitalize()
            updated_recipe_instructions[index] = '. '.join(sentence.capitalize() for sentence in temp_step.split('. '))

pp.pprint(updated_recipe_parsed_ingredients)
print(updated_recipe_instructions)
print(updated_recipe_prep_time)