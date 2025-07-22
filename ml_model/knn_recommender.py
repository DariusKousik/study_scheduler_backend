from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class KNNRecommender:
    def __init__(self, n_neighbors=5):
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
        self.task_titles = []
        self.fitted = False

    def train(self, task_titles):
        if not task_titles:
            return
        self.task_titles = task_titles
        X = self.vectorizer.fit_transform(task_titles)
        self.knn.fit(X)
        self.fitted = True

    def recommend(self, new_task_title):
        if not self.fitted or not self.task_titles:
            return []
        X_new = self.vectorizer.transform([new_task_title])
        distances, indices = self.knn.kneighbors(X_new)
        return [self.task_titles[idx] for idx in indices.flatten()]
