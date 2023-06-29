import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample DataFrame


df = pd.read_csv("jeroen_meus.csv")

# print(df)

# Create a vectorizer and compute the TF-IDF matrix
vectorizer = TfidfVectorizer()
# ingredients_text = df['ingredients'].apply(lambda x: ' '.join(x))


# print(df['ingredients'])

tfidf_matrix = vectorizer.fit_transform(df['ingredients'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get similar recipes based on recipe name
def get_similar_recipes(recipe_name, num_results=1):
    recipe_index = df[df['recipe_name'] == recipe_name].index[0]
    similarity_scores = list(enumerate(cosine_sim[recipe_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similar_recipes = similarity_scores[1:num_results+1]  # Exclude the recipe itself
    similar_recipe_indices = [recipe[0] for recipe in similar_recipes]
    return df.iloc[similar_recipe_indices]

# Example usage
query_recipe = 'Groentelasagne met vier kazen'
similar_recipes = get_similar_recipes(query_recipe)
print(f"Recipes similar to '{query_recipe}':")
print(similar_recipes)
