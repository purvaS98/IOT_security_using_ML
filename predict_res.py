import pickle

def predict(processed_data):

    loaded_model = pickle.load(open(attack_ensemble_model.sav, 'rb'))
    result = loaded_model.score(loaded_model.y1_test, loaded_model.y_pred_ensemble) #y1_test, y_pred_ensemble
    #result = model.predict(data)
    return result