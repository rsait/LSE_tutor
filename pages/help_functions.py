import numpy as np
from scipy.linalg import norm

def selected_features(features_to_select, flatten=True):
    """
    Given the string with the features to select, return de indices of the selected features.

    :param features_to_select: the features to select (extracted from the model name, example: DisTS_WRIST_DIP)
    :type features_to_select: str
    :return: the sorted array of indices to select and an array of distances to add (TIPS, THUMB_TIP)
    :rtype: int array, str array

    :Example:

    ::

        >>> from apps.help_functions import selected_features
        >>> sel_index, dists = selected_features("DisTHUMB_DIP_TIP")
    """
    actual_selected = np.array([],dtype=int)
    add_sel = []
    num_joints = 21
    if flatten: # x,y,z en una dimension, 63 valores
        coords = [0,num_joints,2*num_joints]
        num_joints = num_joints*3
    else: # [21,3], x,y,z en cada zutabe
        # num_joints = 21
        coords = [0]
        #x,y,z = 0,num_joints, 2*num_joints
    if ('DisTS' in features_to_select and 'DisTHUMB' in features_to_select):
        actual_selected = np.append(actual_selected, range(num_joints,num_joints+4))
        actual_selected = np.append(actual_selected, range(num_joints+4,num_joints+2*4-1))
        add_sel = ["TIPS", "THUMB_TIP"]
    elif ('DisTS' in features_to_select):
        actual_selected = np.append(actual_selected, range(num_joints,num_joints+4))
        add_sel = ["TIPS"]
    elif('DisTHUMB' in features_to_select):
        actual_selected = np.append(actual_selected,range(num_joints,num_joints+4))
        add_sel = ["THUMB_TIP"]
    if('WRIST' in features_to_select):
        actual_selected = np.append(actual_selected,coords)
    if('MCP' in features_to_select):
        ind = [4*i+1+coord for i in range(0,5) for coord in coords]
        actual_selected = np.append(actual_selected,ind)
    if('PIP' in features_to_select):
        ind = [4*i+2+coord for i in range(0,5) for coord in coords]
        actual_selected = np.append(actual_selected,ind)
    if('DIP' in features_to_select):
        ind = [4*i+3+coord for i in range(0,5) for coord in coords]
        actual_selected = np.append(actual_selected,ind)
    if('TIP' in features_to_select):
        ind = [4*i+coord for i in range(1,6) for coord in coords]
        actual_selected = np.append(actual_selected,ind)

    actual_selected = np.sort(actual_selected)
    return actual_selected, add_sel


# Buscar el mejor clasificador
# Si es de configuraciones (model_type=='configs') devuelve el path del fichero del modelo, y los
# índices de los features a usar, más la info de qué distancias se han sumado
# Si es el de signos (model_type =='signs') devuelve el path a los HMM, el path al modelo de configuraciones usado 
# y como antes, los features a usar
def best_clf(path, model_type='configs', flatten=True):
    if(model_type == 'configs'):
        file_accuracies = path + "trained_models_accuracies.txt"
        model_type_path = 'models/'
        extension = ".sav"
        features_from = 1 #en el nombre del modelo, desde donde coger los features 3NN_DIP_TIP...
    else: #model_type='signs'
        file_accuracies = path + "trained_HMM_models_accuracies.txt"
        model_type_path = 'hmm_models/'
        extension = ".pkl"
        features_from = 2 #como por delante pone HMM y el clasificador, coger desde el 2 despues del split el nombre del modelo

    with open(file_accuracies) as this_file:
        text_file = [line for x,line in enumerate(this_file) if line!="\n"]
        tuples_list = [tuple((item.split(":")[0], float(item.split(":")[1]))) for item in text_file]
        ordered_list=sorted(tuples_list, key = lambda x: float(x[1]), reverse = True)
        best = ordered_list[0][0]
        best_model = path + model_type_path + best + extension

        features_to_select = best.split("_")[features_from:]
        best_features_index, added_dist = selected_features(features_to_select,flatten)
        # print("BEST MODEL", best_model)
        # print("FEATURES", features_to_select)
        # print("FEATURES INDEX", best_features_index)
    if (model_type == 'configs'):
        return best_model, best_features_index, added_dist
    else: #model_type == 'signs'
        best_model_configs = path  + 'models/' + '_'.join(best.split('_')[1:]) + '.sav'
        return best_model, best_model_configs, best_features_index, added_dist

def transform_data(data, flatten=False):
    new_data = data-data[0,:]
    if flatten:
        joints = data.shape[0]
        coords = data.shape[1]
        flattened_data = np.empty(joints*coords)
        flattened_data[0:joints] = new_data[:,0]
        flattened_data[joints:2*joints]=new_data[:,1]
        flattened_data[2*joints:3*joints]
        return flattened_data
    else:
        return new_data

def dist_between_points(point1, point2, depth):
    """
    Calculate the distances between 2 points.

    :param point1: point with (x,y,z) values
    :type point1: 1D array of length 3
    :param point2: point with (x,y,z) values
    :type point2: 1D array of length 3
    :param depth: indicate whether z-coordinate is used to calculate the distance or not
    :type depth: bool
    :return: the distance between the two points

    :Example:

    ::

        >>> from apps.data_functions import dist_between_points
        >>> dist_p1_p2 = dist_between_points(p1, p2, False)
    """
    if point1 is None or point2 is None:
        return None
    if depth:
        return norm([point1[0]-point2[0], point1[1]-point2[1], point1[2]-point2[2]])
    else:
        return norm([point1[0] - point2[0], point1[1] - point2[1]])


def distances(data, which_distance, remove_thumb_index=False,depth=False):
    # * Indices 21:25 → distances between fingertips, each with the one next to it
    # * Indices 25:28 → distances from fingertips to thumb tip
    """
    Get more information of the original data (MediaPipeHand joints), distance between joints

    :param data: original data
    :type data: ndarray
    :param which_distance: string indicating which distance to add.  If "TIPS" is indicated, distances between contiguous tips are returned. If "THUMB_TIPS" is indicated, distances between thumb tip and the rest of figertips are returned. 
    :type param: str ["TIPS","THUMB_TIP"]
    :param remove_thumb_index: indicates whether to mantain the thumb_index distance when adding "THUMB_TIP" distances. This is only used if the "TIPS" are already added, so as not to repeat the same value.
    :type remove_thumb_index: bool, default False
    :param depth: indicates if the z-value is used when calculating the distances
    :type depth: bool, default False
    :return: an array with the distances indicated by which_distance param
    :rtype: ndarray

    :Example:

    ::

        >>> from apps.data_functions import distances
        >>> data_new_info = distances(data)
        >>> new_data = np.concatenate((data,data_new_info),axis=1)
    """
    if data.ndim == 1: #if there is a file with just one frame
        data = np.expand_dims(data, axis=0)

    if remove_thumb_index==True:
        k = 3
        new_info = 3
    else: 
        k = 2  
        new_info = 4
    
    new_data = np.empty(shape=(data.shape[0], new_info))
    new_feature_names = np.empty(shape=(new_info))
    joints=21

    for idx, instance in enumerate(data):

        if which_distance == "TIPS":

            points1 =  [[instance[j*4+4], instance[j*4+4+joints],instance[j*4+4+2*joints]] for j in range(1,5)]
            points2 = [[instance[j*4], instance[j*4+joints],instance[j*4+2*joints]] for j in range(1,5)]

            new_data[idx] = [dist_between_points(point1, point2, depth) for point1,point2 in zip(points1,points2)]
            #new_feature_names = ["INDEX_THUMB","MIDDLE_INDEX","RING_MIDDLE","PINKY_RING"]
        
        elif which_distance == "THUMB_TIP":
            
            points1 = [[instance[j*4],instance[j*4+joints],instance[j*4+2*joints]] for j in range(k,6)]
            point2 = [instance[4], instance[4+joints], instance[4+2*joints]]

            new_data[idx] = [dist_between_points(point1, point2, depth) for point1 in points1]
            #new_feature_names = ["INDEX_THUMB", "MIDDLE_THUMB", "RING_THUMB", "PINKY_RING"]
        
    return new_data #, new_feature_names


def add_distances_to_landmarks(actual_instance,added_dist):
    """
    Get the instance with the selected values.

    :param actual_instance: the landmarks values of the right hand for one frame, 1D array of 63 values (21(num_joints)*3(x,y,z))
    :type actual_instance: 1D numpy array
    :param added_dist: str array to indicate if distances have been added as features, and which ones
    :type added_dist: str array, added_dist=[] or added_dist=["TIPS","THUMB_TIP"] or added_dist=["TIPS"] or added_dist=["THUMB_TIP"]
    :return: the landmarks with the added_dist added
    :rtype: 1D array of min 63 values, and max 70 (landmarks+tips+thumb_tip) values

    :Example:

    ::

        >>> from apps.data_functions import add_distances_to_landmarks
        >>> new_data_info_added = add_distances_to_landmarks(landmarks_now, ["TIPS"])
        >>> print(new_data_info_added.shape)
    """

    if(len(added_dist) == 2):
        actual_instance = np.concatenate((actual_instance, distances(actual_instance,"TIPS").flatten()))
        actual_instance = np.concatenate((actual_instance, distances(actual_instance,"THUMB_TIP",remove_thumb_index=True).flatten()))
    else:
        if("TIPS" in added_dist):
            actual_instance = np.concatenate((actual_instance, distances(actual_instance,"TIPS").flatten()))
        elif("THUMB_TIP" in added_dist):
            actual_instance = np.concatenate((actual_instance, distances(actual_instance,"THUMB_TIP",remove_thumb_index=False).flatten()))

    return actual_instance
