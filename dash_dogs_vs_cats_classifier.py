# Image classifier dash application
# python dash_dogs_vs_cats_classifier.py   

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import base64
import predict


DEFAULT_MEDIA_DIRECTORY = 'media'
EXTERNAL_STYLESHEETS = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    }
]

dict_extension_signature = {'png' : '89504e470d0a'
    , 'jpg' : 'ffd8ff'
    , 'jpeg' : 'ffd8ff'
    , 'bmp' : '424d'
    , 'gif' : '47494638'
    }                                                  

def remove_all_file_from_folder(folder_path):
    '''
    Remove all file and subfolder from a folder

    Arguments:
        folder_path (str): folder path

    Returns
        None
    '''
    print('Remove all file from media folder\n\t{}'.format(DEFAULT_MEDIA_DIRECTORY))
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def save_image(name, content):
    '''
    Decode and store a file uploaded with Plotly Dash

    Arguments:
        name (str): image name
        content (str): image content

    Returns
        None
    '''
    image_filepath = os.path.join(DEFAULT_MEDIA_DIRECTORY, name)
    data = content.encode('utf8').split(b';base64,')[1]
    with open(image_filepath, 'wb') as fp:
        print('Save uploaded image\n\t{}'.format(image_filepath))
        fp.write(base64.decodebytes(data))


def check_extension_match_signature(content_base64, extension, header_bytes = 8):
    '''
    Check if the image extension matches the file signature

    Arguments:
        content (str): 
        extension (str): 
        header_bytes (int): 

    Returns:
        match (boolean): True if extension and signature mathces and False otherwise
    '''
    signature_hex = dict_extension_signature[extension]
    signature_byte = bytearray.fromhex(signature_hex)
    signature_base64 = base64.b64encode(signature_byte).decode()

    #print(signature_hex)
    #print(base64.b64decode(content_base64).hex()[0:len(signature_hex)]) 

    if signature_hex == base64.b64decode(content_base64).hex()[0:len(signature_hex)]:
        return True
    else:
        return False
            

def is_file_ok(name, content):
    '''
    Check the content of an image

    Arguments:
        name (str): image name
        content (str): image content

    Returns
        ok (boolean): True if the image is ok and False otherwise
    '''
    file_name, extension = name.rsplit('.', 1)
    if extension not in ['png', 'gif', 'jpg', 'jpeg', 'bmp']:
        return False
    else:
        file_type, rest = content.split('/', 1)
        image_type, rest = rest.split(';', 1)
        base, rest = rest.split(',', 1)
        #print(file_type)
        #print(image_type)
        #print(base)
        if file_type != 'data:image' or image_type not in ['png', 'gif', 'jpg', 'jpeg', 'bmp'] or base != 'base64' :
            return False
        else:
            return check_extension_match_signature(rest, extension)


def get_encoded_image(image_filepath):
    '''
    Get image encoded using base64

    Arguments:
        image_filepath (str): image filepath

    Returns
        encoded image(str): encoded image in string format
    '''
    encoded_image = base64.b64encode(open(image_filepath, 'rb').read())
    file_name, extension = image_filepath.rsplit('.', 1)
    return 'data:image/{};base64,{}'.format(extension.lower(), encoded_image.decode())


def _create_app():
    ''' 
    Creates dash application

    Arguments:
        None

    Returns:
        app (dash.Dash): Dash application
    '''
    app = dash.Dash(__name__, external_stylesheets = EXTERNAL_STYLESHEETS)

    print('Check if media folder present and if not create it\n\t{}'.format(DEFAULT_MEDIA_DIRECTORY))
    if not os.path.exists(DEFAULT_MEDIA_DIRECTORY):
        os.makedirs(DEFAULT_MEDIA_DIRECTORY)

    sample_training_dataset = predict.get_sample_from_training_dataset()

    app.layout = html.Div(
        [
        dbc.Nav(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.A('Dogs vs Cats Classifier Application', href='/', className = 'navbar-brand' )
                            ], className = 'navbar-header')
                        , html.Div(
                            [
                                html.Ul(
                                    [
                                       html.Li(html.A('Github', href='https://github.com/simonerigoni/kaggle'))
                                    ], className = 'nav navbar-nav')
                            ], className = 'collapse navbar-collapse')
                    ], className = 'container')
            ], className = 'navbar navbar-inverse navbar-fixed-top')
            , html.Div(
                [
                    html.H1('Dogs vs Cats Classifier Application', className = 'text-center')
                    , html.P('Classify Images of Dogs and Cats', className = 'text-center')
                    , html.Hr()
                    , html.Div(
                        [
                            #html.Div(
                            #    [
                                    dcc.Upload(id = 'upload-image', children = html.Div(['Drag and Drop or ', html.A('Select File')]),
                                        style = {
                                            'width': '98%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple = True
                                    )
                                    , html.Div(id = 'output-image-upload')
                                    , html.Hr()
                                    , html.Button('Classify Image', id = 'button-submit', className = 'btn btn-lg btn-success')
                                #] , className = 'row')
                        ] , className = 'container')
                ], className = 'jumbotron')
            , html.Div(id = 'results')
    ] , className = 'container')


    def parse_contents(contents, filename, date):
        ''' 
        Parse loaded image

        Arguments:
            contents (str): image content in binary form
            filename (str): image filename
            date (str): loading image timestap 

        Returns:
            html.div (dash_html_components.Div): div containing the input image
        '''
        return html.Div([
            #html.H5(filename)
            #, html.H6(datetime.datetime.fromtimestamp(date))
            ## HTML images accept base64 encoded strings in the same format that is supplied by the upload
            # ,
            html.Img(src = contents, style = {'height':'50%', 'width':'50%'})
            #, html.Hr()
            #, html.Div('Raw Content')
            #, html.Pre(contents[0:200] + '...', style = {'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'})
        ])


    @app.callback(dash.dependencies.Output('output-image-upload', 'children'), [dash.dependencies.Input('upload-image', 'contents')], [dash.dependencies.State('upload-image', 'filename'), dash.dependencies.State('upload-image', 'last_modified')])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        '''
        Show loaded image

        Arguments:
            list_of_contents (list): list of uploaded images content
            list_of_names (list): list of uploaded images names
            list_of_dates (list): list of images loading timestap 

        Returns:
            children (dash_html_components.Div): html div to be updated
        '''
        if list_of_contents is not None:
            content = list_of_contents[0]
            name = list_of_names[0]
            date = list_of_dates[0]
            if is_file_ok(name, content):
                children = parse_contents(content, name, date)
                save_image(name, content)
            else:
                children = html.Div('An error occurred: Accepted only png, gif, jpg, jpeg or bmp image')
            return children

    @app.callback(dash.dependencies.Output('results','children'), [dash.dependencies.Input('button-submit', 'n_clicks')])
    def update_results(n_click):
        '''
        Update the results section 

        Arguments:
            n_click (int): value of n_clicks of button-submit

        Returns:
            results (list): list of dash components 
        '''
        results = []
        files = os.listdir(DEFAULT_MEDIA_DIRECTORY)
        number_of_classes = predict.get_number_of_classes()

        if len(files) == 0:
            results.append(html.Div(
                [
                    html.H2('Overview of Training Dataset', className='text-center')
                    , html.H3('{} classes'.format(number_of_classes), className = 'text-center')
                ]))

            buffer_images = []
            for category, image in sample_training_dataset:
                #results.append(html.Div([html.Img(src = get_encoded_image(sample_training_dataset[category]), style = {'height':'20%', 'width':'20%'}), html.H5(category)])) 
                if len(buffer_images) == 4:
                    #print(buffer_images[0], buffer_images[1], buffer_images[2], buffer_images[3])
                    results.append(html.Div([
                        html.Div([html.Img(src = get_encoded_image((buffer_images[0])[1]), style = {'height':'75%', 'width':'75%'}), html.H5((buffer_images[0])[0])], className = 'col-sm-3')
                        , html.Div([html.Img(src = get_encoded_image((buffer_images[1])[1]), style = {'height':'75%', 'width':'75%'}), html.H5((buffer_images[1])[0])], className = 'col-sm-3')
                        , html.Div([html.Img(src = get_encoded_image((buffer_images[2])[1]), style = {'height':'75%', 'width':'75%'}), html.H5((buffer_images[2])[0])], className = 'col-sm-3')
                        , html.Div([html.Img(src = get_encoded_image((buffer_images[3])[1]), style = {'height':'75%', 'width':'75%'}), html.H5((buffer_images[3])[0])], className = 'col-sm-3')
                    ], className = 'row'))
                    buffer_images = []
                buffer_images.append((category, image))
        else:
            image_filepath = DEFAULT_MEDIA_DIRECTORY + '/' + files[0]
            print('Classify image\n\t{}'.format(image_filepath))
            predict_response = predict.get_prediction(image_filepath)
            
            if isinstance(predict_response, str):
                print(predict_response)
                results.append(html.Div(
                    [
                        html.H2('Classification', className='text-center')
                        , html.H1(predict_response, className='text-center')
                    ]))
            else:
                results.append(html.Div(
                    [
                        html.H2('Classification', className='text-center')
                        , html.H1(predict_response.payload[0].display_name, className='text-center')
                        , html.H1('Score: {0:.2f}'.format(predict_response.payload[0].classification.score), className='text-center')
                    ]))

            remove_all_file_from_folder(DEFAULT_MEDIA_DIRECTORY)
        return results

    return app


if __name__ == '__main__':
    app = _create_app()
    app.run_server(debug = True)