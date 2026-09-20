import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# 1. Load and prepare data
df = pd.read_csv("G1_15.csv")

# Fill missing keyword values with empty strings
df['Author Keywords'] = df['Author Keywords'].fillna('')
df['Index Keywords'] = df['Index Keywords'].fillna('')

# Combine fields for rich semantic context
df['processed_text'] = (
    df['Title'].astype(str) + ". " + 
    df['Abstract'].astype(str) + " Keywords: " + 
    df['Author Keywords'].astype(str)
)

docs = df['processed_text'].tolist()

# 2. Configure modular BERTopic sub-models
# Pre-trained scientific/transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Dimensionality reduction (reproducible with random_state)
umap_model = UMAP(
    n_neighbors=15, 
    n_components=5, 
    min_dist=0.0, 
    metric='cosine', 
    random_state=42
)

# Density-based clustering
hdbscan_model = HDBSCAN(
    min_cluster_size=30, 
    metric='euclidean', 
    cluster_selection_method='eom', 
    prediction_data=True
)

# Custom CountVectorizer to remove standard & domain-specific stop words
vectorizer_model = CountVectorizer(
    stop_words="english", 
    ngram_range=(1, 2), 
    min_df=5
)

# 3. Initialize and fit BERTopic
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    top_n_words=10,
    verbose=True
)

topics, probs = topic_model.fit_transform(docs)

# 4. Attach topic results back to original DataFrame
df['Topic'] = topics
df['Topic_Probability'] = probs

# 5. Extract topic summary table
topic_info = topic_model.get_topic_info()
print(topic_info.head(15))

# Export results for analysis and paper tables
df.to_csv("iot_security_with_topics.csv", index=False)
topic_info.to_csv("iot_security_topic_summary.csv", index=False)