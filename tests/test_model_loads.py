def test_vectorizer_load():
    import joblib
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    assert vectorizer is not None

def test_model_load():
    import joblib
    model = joblib.load("models/isolation_forest_model.pkl")
    assert model is not None
