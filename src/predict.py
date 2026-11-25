# Uses a trained GCP model to predict the class for an input image
# python -m src.predict
# python -m src.predict --image_path data/test/2.jpg

import argparse
import os

from google.cloud import automl_v1beta1
from google.oauth2 import service_account

from src.config import (
    CREDENTIALS_JSON_FILE_PATH,
    DEFAULT_TEST_IMAGE,
    GCP_FOLDER,
    MODEL_ID,
    PROJECT_ID,
)

__all__ = [
    "CREDENTIALS_JSON_FILE_PATH",
    "DEFAULT_TEST_IMAGE",
    "GCP_FOLDER",
    "MODEL_ID",
    "PROJECT_ID",
    "get_number_of_classes",
    "get_prediction",
    "get_sample_from_training_dataset",
    "parse_input_arguments",
]


def parse_input_arguments():
    """
    Parse input arguments

    Arguments:
        None

    Returns:
        image_path (str): image path to classify. Default value DEFAULT_TEST_IMAGE
    """
    parser = argparse.ArgumentParser(description="Predict using a GCP model")
    parser.add_argument("--image_path", type=str, default=DEFAULT_TEST_IMAGE, help="Dataset path")

    args = parser.parse_args()
    # print(args)

    return args.image_path


def get_number_of_classes():
    """
    Return the number of classes used

    Arguments:
        None

    Returns:
        number_of_classes (int): number of classes used
    """
    labels = []
    for label_directory in os.listdir(GCP_FOLDER):
        if os.path.isfile(GCP_FOLDER + "/" + label_directory):
            pass
        else:
            labels.append(label_directory)
    return len(labels)


def get_sample_from_training_dataset(number_of_samples=40):
    """
    Get a sample from the training dataset

    Arguments:
        number_of_samples (int): number of sample from the train dataset

    Returns:
        category_sample (dict): dictonary with category and image path
    """
    category_sample = []
    for label_directory in os.listdir(GCP_FOLDER):
        if os.path.isfile(GCP_FOLDER + "/" + label_directory):
            pass
        else:
            for filename in os.listdir(GCP_FOLDER + "/" + label_directory)[
                : round(number_of_samples / get_number_of_classes())
            ]:
                # print(label_directory, GCP_FOLDER + '/' + label_directory + '/' + filename)
                category_sample.append(
                    (label_directory, GCP_FOLDER + "/" + label_directory + "/" + filename)
                )
    return list((category, sample) for category, sample in category_sample)


def get_prediction(
    image_file_path,
    credentials_json_file_path=CREDENTIALS_JSON_FILE_PATH,
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
):
    """
    Get prediction

    Arguments:
        image_file_path: image to classify file path
        credentials_json_file_path:
        project_id:
        model_id:

    Returns:
        request: classification
    """

    if not credentials_json_file_path or not project_id or not model_id:
        return "Error: GCP credentials are not configured"

    with open(image_file_path, "rb") as ff:
        content = ff.read()

        credentials = service_account.Credentials.from_service_account_file(
            credentials_json_file_path
        )
        prediction_client = automl_v1beta1.PredictionServiceClient(credentials=credentials)

        name = f"projects/{project_id}/locations/us-central1/models/{model_id}"
        payload = {"image": {"image_bytes": content}}
        params = {}
        try:
            # google-cloud-automl now takes a single request / keyword args
            request = prediction_client.predict(
                request={"name": name, "payload": payload, "params": params}
            )
        except Exception as e:
            request = f"Error: {e}"

        return request  # waits till request is returned


if __name__ == "__main__":
    image_path = parse_input_arguments()
    # print(image_path)

    # print(get_number_of_classes())
    # print(get_sample_from_training_dataset())

    predict_response = get_prediction(image_path)

    if isinstance(predict_response, str):
        print(predict_response)
    else:
        print(
            f"Image {image_path} classified as {predict_response.payload[0].display_name} with score {predict_response.payload[0].classification.score}"
        )
