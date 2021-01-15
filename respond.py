# For loading machine learning model
import pickle
import numpy as np

with open ("DT_model.pkl", 'rb') as file:
    clf = pickle.load(file)
    

responses = {1: "Mostly CoVID, see a doctor quickly.",
             2: "Mostly Influenza, see a doctor quickly.",
             3: "Mostly CoVID, take an antipyretic and if the condition persists, go to a doctor.",
             4: "Mostly Influenza, take an antipyretic and if the condition persists, go to a doctor.",
             5: "Mostly CoVID, take Paracetamol and if the condition persists, go to a doctor.",
             6: "Mostly Influenza, take Paracetamol and if the condition persists, go to a doctor.",
             7: "Unclear case but take Paracetamol and rest.",
             8: "Unclear case but take an antipyretic for the fever.",
             9: "Could be asthma or chronic obstructive pulmonary disease, please take your medications.",
             10:"Could be sinusitis, if the condition persists, go to a doctor.",
             11: "Mostly common cold, no need to worry and no need to take medications.",
             12: "No need to panic, take a bronchodilator and live normally.",
             13: "No need to panic, take Paracetamol and live normally.",
             14: "No need to worry, take a throat lozenges and live normally.",
             15: "No need to worry and no need to take medications.",
             16: "If it is exercise-induced, just rest, otherwise take a muscle relaxant.",
             17: "Just rest a bit.",
             18: "Why are you even here?"}

def respond(list_or_array):
    """
    Takes a list or array of inputs and return a response

    Parameters
    ----------
    list_or_array : list or ndarray

    Returns
    -------
    response as string.

    """
    global responses
    global clf
    
    # Check for a right data format
    if type(list_or_array) == type([]):
        list_or_array = np.array(list_or_array, dtype = np.uint8).reshape(1,-1)
    elif type(list_or_array) == type(()):
        list_or_array = np.array(list_or_array, dtype = np.uint8).reshape(1,-1)
    elif type(list_or_array) == type(np.array([])):
        pass
    else:
        return "Error, unsupported list format"
    
    # Check for correct data size
    if list_or_array.shape[1] != 9:
        return "Error, size of data not supported"
    
    y_predict = clf.predict(list_or_array)
    return responses[y_predict[0]]
