class Uploader():
    def __init__(self, kaggle_json):
        assert os.path.isfile(kaggle_json) == True


        
        os.system("mkdir -p ~/.kaggle")
        os.system(f"cp {kaggle_json} ~/.kaggle/")
        os.system("chmod 600 ~/.kaggle/kaggle.json")
        os.system("ls ~/.kaggle")

        os.system("ls -l ~/.kaggle")
        os.system("cat ~/.kaggle/kaggle.json")

        os.system("pip install --upgrade --force-reinstall --no-deps kaggle")


    def create_dataset(self):
        pass

    def update_version(self):
        pass 


    def preview_directory_structure(self):
        pass
        

    def prepare_dataset(self):
        pass



if __name__ != "__main__":
    import os 
    import shutil 
    from zipfile import ZipFile 

