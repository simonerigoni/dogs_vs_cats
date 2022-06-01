# Uses a trained GCP model to predict the class for an input image
# python predict.py
# python predict.py --image_path data/test/2.jpg

import os
import argparse

from google.cloud import automl_v1beta1
from google.oauth2 import service_account


BASE_DATA_DIRECTORY = 'data/'
KAGGLE_DATA = BASE_DATA_DIRECTORY + 'kaggle/train/'
GCP_DATA = BASE_DATA_DIRECTORY + 'gcp/'
DEFAULT_TEST_IMAGE = BASE_DATA_DIRECTORY + '/test/1.jpg'
CREDENTIALS_JSON_FILE_PATH = 'YOUR_CREDENTIALS_JSON_FILE_PATH'
PROJECT_ID = 'YOUR_PROJECT_ID'
MODEL_ID = 'YOUR_MODEL_ID'


def parse_input_arguments():
    '''
    Parse input arguments

    Arguments:
        None

    Returns:
        image_path (str): image path to classify. Default value DEFAULT_TEST_IMAGE
    '''
    parser = argparse.ArgumentParser(description = "Predict using a GCP model")
    parser.add_argument('--image_path', type = str, default = DEFAULT_TEST_IMAGE, help = 'Dataset path')

    args = parser.parse_args()
    #print(args)

    return args.image_path


def get_number_of_classes():
    '''
    Return the number of classes used

    Arguments:
        None

    Returns:
        number_of_classes (int): number of classes used
    '''
    labels = []
    for label_directory in os.listdir(GCP_DATA):
        if os.path.isfile(GCP_DATA + '/' + label_directory):
            pass
        else:
            labels.append(label_directory)
    return len(labels)


def get_sample_from_training_dataset(number_of_samples = 40):
    '''
    Get a sample from the training dataset

    Arguments:
        number_of_samples (int): number of sample from the train dataset

    Returns:
        category_sample (dict): dictonary with category and image path
    '''
    category_sample = []
    for label_directory in os.listdir(GCP_DATA):
        if os.path.isfile(GCP_DATA + '/' + label_directory):
            pass
        else:
            for filename in os.listdir(GCP_DATA + '/' + label_directory)[:round(number_of_samples / get_number_of_classes())]:
                #print(label_directory, GCP_DATA + '/' + label_directory + '/' + filename)
                category_sample.append((label_directory, GCP_DATA + '/' + label_directory + '/' + filename))
    return list((category, sample) for category, sample in category_sample) 


def get_prediction(image_file_path, credentials_json_file_path = CREDENTIALS_JSON_FILE_PATH, project_id = PROJECT_ID, model_id = MODEL_ID):
    '''
    Get prediction

    Arguments:
        image_file_path: image to classify file path
        credentials_json_file_path:
        project_id:
        model_id:

    Returns:
        request: classification
    '''

    with open(image_file_path, 'rb') as ff:
        content = ff.read()

        credentials = service_account.Credentials.from_service_account_file(credentials_json_file_path)
        prediction_client = automl_v1beta1.PredictionServiceClient(credentials = credentials)

        name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
        payload = {'image': {'image_bytes': content }}
        params = {}
        try:
            request = prediction_client.predict(name, payload, params)
        except Exception as e: 
            request = 'Error: {}'.format(e)

        return request  # waits till request is returned


if __name__ == "__main__":
    image_path = parse_input_arguments()
    # print(image_path)

    #print(get_number_of_classes())
    #print(get_sample_from_training_dataset())

    predict_response = get_prediction(image_path)
    
    if isinstance(predict_response, str):
        print(predict_response)
    else:
        print('Image {} classified as {} with score {}'.format(image_path, predict_response.payload[0].display_name, predict_response.payload[0].classification.score))

