from PIL import Image
import warnings
import numpy as np
import math
import time
import json
import numpy as np
import base64
import requests
import os


class Athena:

    def predict(self, api_key=None, learning_object=None, inference=None, use_prebuilt=False, allow_keep=False, trial=False):
        '''
        --------------------------
        Use Athena to make a prediction with input examples or the prebuilt model.
        --------------------------
        Params:

          - api_key (string):
              The api key for your clevrML developer account.

          - input_object (dictionary):
              An dictionary with reference examples. These reference examples will be
              used for Athena to make a prediction.
          
          - use_prebuilt (Boolean):
              Use the prebuilt model for a prediction. Set this param to True if you 
              want to use the prebuilt classes, otherwise set to False.
          
        --------------------------
        Example:

          from clevrml_earlyaccess import Athena

          Athena().predict(
            api_key="key12345",
            learning_object={
                "image": [
                       ["dog1.jpg", "dog"],
                       ["dog2.jpg", "dog"],
                       ["cat1.jpg", "cat"],
                       ["cat2.jpg", "cat"]
                ]
            },
            use_prebuilt=False
          )

        '''
        
        if api_key == None:
            raise Exception('Please enter your api key to use the clevrML MPL API')
        
        if learning_object == None and inference == None:
            raise Exception('Please pass an object through the "input object" or "inference" parameter to make a prediction.')
        

        else:
            image_bytes = []
            request_object = {'inference': {}}

            if use_prebuilt == False:
                for key, val in learning_object.items():

                    if key == 'categorical':
                        categorical_ob = {'label_data': []}
                        cat_tmp = []
                        classes = []
                        
                        for values in val:
                            cat_tmp.append(values[:-1])
                            classes.append(values[-1])
                            
                            if values[-1] in categorical_ob['label_data']:
                                continue
                            else:
                                categorical_ob['label_data'].append(values[-1])

                        
                        flat = [item for sublist in cat_tmp for item in sublist]
                        categorical_ob['data'] = flat
                        categorical_ob['classes'] = classes
                        request_object['categorical'] = categorical_ob
                            

                    if key == 'image':
                        request_object['image'] = {}
                        tmp = []

                        for iter in learning_object[key]:
                            image_file = Image.open(iter[0])
                            image_size = image_file.size
                            x = round(image_size[0] * 0.5)
                            y = round(image_size[1] * 0.5)

                            image_file = image_file.resize((x,y),Image.ANTIALIAS)
                            image_file.save(iter[0],quality=95)
                            image_file.save(iter[0],optimize=True,quality=95)

                            with open(iter[0], 'rb') as f:
                                meta = f.read()
                                byte_data = base64.encodebytes(meta).decode("utf-8")
                                
                                if iter[1] in request_object['image']:
                                    request_object['image'][iter[1]].append(byte_data)
                                else:
                                    request_object['image'][iter[1]] = []
                                    request_object['image'][iter[1]].append(byte_data)

                            f.close()


                    if key == 'text':
                          request_object['text'] = {}

                          for iters in learning_object[key]:
                              if iters[1] in request_object['text']:
                                  request_object['text'][iters[1]].append(iters[0])
                              else:
                                  request_object['text'][iters[1]] = []
                                  request_object['text'][iters[1]].append(iters[0])

                    
                    for kay, vals in inference.items():

                        if kay == 'categorical':
                            request_object['inference']['categorical'] = vals
  
                        if kay == 'text':
                            if 'text' in request_object['inference']:
                                request_object['inference']['text'].append(vals)
                            else:
                                request_object['inference']['text'] = [vals]
                        
                        if kay == 'image':
                            image_file = Image.open(vals)
                            image_size = image_file.size
                            x = round(image_size[0] * 0.5)
                            y = round(image_size[1] * 0.5)

                            image_file = image_file.resize((x,y),Image.ANTIALIAS)
                            image_file.save(vals,quality=95)
                            image_file.save(vals,optimize=True,quality=95)

                            with open(vals, 'rb') as f:
                                meta = f.read()
                                byte_data = base64.encodebytes(meta).decode("utf-8")

                                if 'image' in request_object['inference']:
                                    request_object['inference']['image'].append(byte_data)
                                else:
                                    request_object['inference']['image'] = [byte_data]
                            
                            f.close()


        payload = {
              'api_key': api_key,
              'request_object': request_object,
              'use_prebuilt': use_prebuilt,
              'allow_keep': allow_keep,
              'trial': trial
          }

        
        print('Sending request...')

        url = "https://earlyaccess.api.clevrml.com/athena/v1/predict"
        r = requests.post(url, data=json.dumps(payload))
        
        try:
            response = json.loads(r.text)
            if 'Status' in response:
                raise Exception('You have used your free tier for the Athena API Beta. Please do one of the following:')
            if response['status'] == 'Success':
                print(json.dumps(response, sort_keys=True, indent=4))

                return response['return_object']['prediction']
            
            else:
  
                print(response)

        except Exception as e:
            print(e)
            print(r.text)

          