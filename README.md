# Dogs vs Cats with Google AutoML

## Introduction

The goal of the project is to use [Google AutoML](https://cloud.google.com/automl) to classify whether images contain either a dog or a cat.

## Software and Libraries

This project uses Python 3.11 and the most important packages are:

* [Google Cloud](https://pypi.org/project/google-cloud/)
* [dash](https://plot.ly/dash/)

## Local configuration

To setup a new local enviroment and install all dependencies you can run `.\my_scripts\Set-Up.ps1`. It will install:

* [Python](https://www.python.org/)
* [uv](https://docs.astral.sh/uv/)
* [Pre-commit](https://pre-commit.com/)

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. A pre-commit hook is a script that runs before a commit operation in a version control system. This allows to shift left code quality checks and remediations. You can change the hooks by updateing the file `.pre-commit-config.yaml`.

To trigger the pre-commit hooks without an actual commit you can run `pre-commit run --all-files -v`.

## Data

Have a look at the `data` folder and its [DATA.md](data/DATA.md) file.

## Testing

No test implemented.

## Running the code

The code for generating the `all_data.csv` to map the images to let Google AutoML Vision generate a model is provided in the [Jupyter Notebook](http://ipython.org/notebook.html) _dogs_vs_cats.ipynb_

If you download it simply run the command `jupyter notebook dogs_vs_cats.ipynb` in the folder were the file is located

From the project folder run `python dash_app.py` to start the dash application. The default url to connect to it is http://127.0.0.1:8050/

## Results

The dash application 

![Home](images/home.JPG)

When no image is give in input the application gives an overview of the dataset in the home page

When an image is submitted with the **Classify Message** button the resulting category is shown

![Classification Result](images/classification_result.JPG)

## List of activities

In the [TODO.md](TODO.md) file you can find the list of tasks and on going activities.

## Licensing and Acknowledgements

Have a look at [LICENSE.md](LICENSE.md) and many thanks to [Kaggle](https://www.kaggle.com/) for the dataset.

## Outro

I hope this repository was interesting and thank you for taking the time to check it out. On my Medium you can find a more in depth [story](https://medium.com/@simone-rigoni01/classify-dogs-and-cats-with-google-automl-2ae6eac64117) and on my Blogspot you can find the same [post](https://simonerigoni01.blogspot.com/) in italian. Let me know if you have any question and if you like the content that I create feel free to [buy me a coffee](https://www.buymeacoffee.com/simonerigoni).