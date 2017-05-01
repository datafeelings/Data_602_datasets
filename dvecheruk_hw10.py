# -*- coding: utf-8 -*-
"""
CUNY DATA 602 Homework 10: Matplotlib

Created on Sun Apr 30 20:39:53 2017

@author: Dmitriy Vecheruk

Assignment:  

1.  Express the cars.data.csv data as a series of bar graphs.  The x-axis represents 
    a feature and the y-axis is the frequency in the sample.  
    Do this with the 'buying', 'maint', 'safety', and 'doors' fields with one plot 
    for each for a total of four.  Make each graph a subplot of a single output.
2.  Plot your results from the linear regression in homework 5 and 7 
    (for any of the provided data sets).  The plot should include.  
    1) a scatter of the points in the .csv file 
    2) a line showing the regression line (either from the calculation in homework 5 
    or line-fitting from homework 7).  
    3) something on the plot that specifies the equation for the regression line.
3.  Create an overlay of the center points found in objects.png from homework 8.  
    The image should be in the background and the object centers can be small 
    circles or points at or around the center points.
4.  Plot a line graph that shows the hour by hour change in number of server requests 
    from the HTTP in homework 9.  The x-axis is the discrete hour intervals (e.g. 13:00 – 14:00) and the y-axis is the number of requests. 
    
    
Reference:
 Course reading and video
 http://stackoverflow.com/questions/31029560/plotting-categorical-data-with-pandas-and-matplotlib
 http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
 http://stackoverflow.com/questions/35376572/reading-image-from-url-with-misc-imread-returning-a-flattened-array-instead-of-a
"""

###### 1. Car data plots ######

print ' \n Figure for the cars dataset \n'

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'https://raw.githubusercontent.com/datafeelings/Data_602_datasets/master/cars.data.csv'

cars = pd.read_csv(data_path, header=None)
cars.columns = ['bying','maint','doors','persons','lug_boot', 'safety', 'accept']

def plot_bars(var):
    '''
    Plots a Tukey-style barchart with counts of frequencies of a grouping
    variable in the cars dataset, takes variable name as input and returns a 
    pyplot into the environment
    '''
    
    cars.groupby(var).size().plot(kind='bar')
    m = cars.groupby(var).size().max()
    plt.yticks(range(0,m,50))
    plt.grid(True, axis='y', color='w')
    

plt.figure(figsize=(8, 6))
plt.suptitle('Frequencies of values in the cars dataset')       
plt.subplot(221) 
plot_bars('bying')
plt.subplot(222)
plot_bars('maint')
plt.subplot(223)
plot_bars('safety')
plt.subplot(224)
plot_bars('doors')
plt.subplots_adjust(hspace=1, wspace=0.5)
plt.show()
    
###### 2. Linear regression plot ######

print ' \n Figure for the linear regression \n'

def read_json_from_url(url):
    '''
    Reads json from a specified URL. Returns a dict with JSON contents
    '''

    import urllib, json

    response = urllib.urlopen(url)
    out = json.loads(response.read())
    return out

def lm_eval(lin_mod, x):
    '''
    This function takes a linear model as defined by the lm() function and calculates a new predicted
    value of Y for a given value of X.
    :param lin_mod: output of the lm() function
    :param x: float, value of predictor variable
    :return: float, predicted value of the response variable
    '''

    return x*lin_mod['slope'] + lin_mod['intercept']


def show_lm_plot(linmod):
    '''
    lm_plot() makes a plot of the dataset and the regression line, which is contained in the output of the lm() function
    :param linmod: dict, output of the lm() function
    :return: None
    '''

    try:
        import matplotlib.pyplot as plt
        
        plt.figure()
        plt.plot(linmod['values']['x'], linmod['values']['y'],'bo') # plot values

        min_x = min(linmod['values']['x'])
        min_y = lm_eval(linmod, min_x)
        max_x = max(linmod['values']['x'])
        max_y = lm_eval(linmod, max_x)

        plt.plot([min_x, max_x], [min_y, max_y], 'r--', lw=1) # overlay the regression line
        plt.xlabel(linmod['x_name'])
        plt.ylabel(linmod['y_name'])
        plt.title(linmod['formula'])

        plt.show()
    except KeyError:
        print 'Plot error: Input file is in the wrong format'
    except ImportError:
        print 'Plot error: matplotlib not found'
        

data_path = 'https://raw.githubusercontent.com/datafeelings/Data_602_datasets/master/linmod.json'
linmod = read_json_from_url(data_path)
show_lm_plot(linmod)

###### 3. Figures for the image recognition dataset ######

print ' \n Figure for the image recognition \n'

#input_img_path = 'C:\Users\dima\Google Drive\CUNY_MSDA\Data_602_Python\Week_9\input_images\objects.png'
#img_cm_path = 'C:\Users\dima\Google Drive\CUNY_MSDA\Data_602_Python\Week_9\img2_cm.json'


def display_image_cm(input_img_url, img_cm_url):
    '''
    This function reads and image, and a json with the coordinates of the
    centers of mass in the image and plots an overlay over the image
    
    :param: input_img_path: path to the image
    :param: img_cm_path: path to the json holding the coordinates of cent.mass
    :return: None, returns a plt.figure() into the environment 
    '''
    import scipy.misc as misc
    import urllib2, cStringIO
    
    cm = read_json_from_url(img_cm_url)
    
    file = cStringIO.StringIO(urllib2.urlopen(input_img_url).read())
    raw = misc.imread(file)
    
    x = [item for item in cm['cm'][1]] 
    y = [item for item in cm['cm'][0]]
    
    
    plt.figure()
    plt.title('Centers of Mass for objects.png')
    plt.set_cmap(plt.gray())
    plt.imshow(raw, cmap='gray')
    plt.scatter(y,x, c='r', s=40)
    plt.show()


img_url = 'https://raw.githubusercontent.com/datafeelings/Data_602_datasets/master/objects.png'

cm_url = 'https://raw.githubusercontent.com/datafeelings/Data_602_datasets/master/img2_cm.json'


display_image_cm(img_url, cm_url)

###### 4. Figures for the Pandas log analysis ######

print ' \n Figure for the log analysis \n'

data_path = 'https://raw.githubusercontent.com/datafeelings/Data_602_datasets/master/processed_logs.csv'

logs = pd.read_csv(data_path, header=0)

req_hour= logs.groupby('hour')['request'].count()
plt.figure()
plt.grid(True)
plt.plot(req_hour)
plt.scatter(x = req_hour.index, y = req_hour, marker='o')
plt.title('Count of server requests per hour')
plt.xticks(req_hour.index)
