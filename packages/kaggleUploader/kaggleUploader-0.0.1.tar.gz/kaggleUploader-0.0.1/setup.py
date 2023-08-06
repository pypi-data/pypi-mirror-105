from setuptools import setup, Extension

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'kaggleUploader',         # How you named your package folder (MyLib)
    packages = ['kaggleUploader'],   # Chose the same as "name"
    version = '0.0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Wrapper built on top of kaggle api to help with uploading of datasets to your Kaggle account with minimal and easier interface.',   # Give a short description about your library
    long_description = readme,
    long_description_content_type = 'text/markdown',
    author = 'Antoreep Jana',                   # Type in your name
    author_email = 'antoreepjana@gmail.com',      # Type in your E-Mail
    url = 'https://gitlab.com/antoreep_jana/kaggleuploader/-/tree/master/',   # Provide either the link to your github or to your website
    download_url = 'https://gitlab.com/antoreep_jana/kaggleuploader/-/archive/v0.0.1/kaggleuploader-v0.0.1.tar.gz',    # I explain this later on
    keywords = ['Kaggle Uploader' , 'Kaggle Dataset Uploader', 'dataset uploader' , 'Google Colab', 'kaggle dataset upload google colab' ],   # Keywords that define your package best
    #install_requires=[            # I get to this in a second
    #       
    #    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
