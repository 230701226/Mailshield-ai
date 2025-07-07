def test_vectorizer_load():
    import joblib
    v = joblib.load("models/tfidf_vectorizer.pkl")
    assert v is not None

def test_model_load():
    import joblib
    m = joblib.load("models/isolation_forest_model.pkl")
    assert m is not None
