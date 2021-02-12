import os 
import json
import shutil
import datetime as dt
from zipfile import ZipFile, ZIP_DEFLATED
from src import static
from src.dirs import (
    DATA_DIR,
    SRC_DIR,
    MAIN_DIR
)

class Controller(object):

    def __init__(self,data_dir,verbose=False):
        self.data_dir = data_dir
        self.verbose = verbose
        self.snapshots = []
        self._create_data_dir()
        self._read_config()
        self._read_snapshots()
        static.ascii_art()
        if self.verbose:
            static.config_display(self.config)

    def _create_data_dir(self):
        if 'data' not in os.listdir(MAIN_DIR):
            os.mkdir(os.path.join(MAIN_DIR,'data'))

    def _read_config(self):
        try:
            with open(os.path.join(MAIN_DIR,'config.json')) as f:
                self.config = dict(json.load(f))
        except Exception as e:
            static.config_exception(e)
            quit()

    def _read_snapshots(self):
        for snap_dirname in os.listdir(DATA_DIR):
            try:
                snap_dir = os.path.join(DATA_DIR,snap_dirname)
                with open(os.path.join(snap_dir,'meta.json')) as f:
                    meta =  dict(json.load(f))
                with open(os.path.join(snap_dir,'config.json')) as f:
                    config =  dict(json.load(f))
                snapshot = Snapshot(
                    config=config,
                    message=meta['message'],
                    verbose=self.verbose,
                    snap_dir=snap_dir,
                    date=meta['date'])
                self.snapshots.append(snapshot)
            except Exception as e:
                print('Could not read %s'%snap_dirname)
        self._sort_snapshots()

    def _sort_snapshots(self):
        self.snapshots.sort(
            key=lambda snapshot:dt.datetime.fromisoformat(snapshot.date))

    def create_snapshot(self,message):
        try:
            snapshot = Snapshot(
                config=self.config,
                message=message,
                verbose=self.verbose)
            snapshot.create()
            self.snapshots.append(snapshot)
            self._sort_snapshots()
        except Exception as e:
            static.create_exception(message,e)

    def list_snapshots(self):
        print('Available Snapshots: ')
        for i, snapshot in enumerate(self.snapshots):
            print('\t%s) %s'%(str(i),str(snapshot)))
        print('\n')

    def retrieve_snapshot(self,which):
        try:
            if which == 'latest':
                self.snapshots[-1].retrieve()
            else:
                self.snapshots[int(which)].retrieve()
        except Exception as e:
            static.retrieve_exception(which,e)

    def purge_snapshots(self):
        for snap_dirname in os.listdir(DATA_DIR):
            shutil.rmtree(os.path.join(DATA_DIR,snap_dirname))
        static.purged()

class Snapshot(object):

    def __init__(self,config,message,verbose,snap_dir=None,date=None):
        self.config = config
        self.message = message
        self.verbose = verbose
        self.snap_dir = snap_dir
        self.date = date

    def __str__(self):
        return '%s - "%s"'%(self.date.ljust(10),self.message)

    def _create_snap_dir(self):
        self.date = str(dt.datetime.now())
        self.snap_dir = os.path.join(DATA_DIR,self.date)
        if self.date not in os.listdir(DATA_DIR):
            os.mkdir(self.snap_dir)

    def create(self):

        # create snapshot directory 
        self._create_snap_dir()
        static.build_snapshot(self.date)

        # save content to zip files and push to snapshot data directory
        for name,dir in self.config.items():
            file_paths = []
            for root, directories, files in os.walk(dir): 
                for filename in files: 
                    file_paths.append(os.path.join(root, filename))
            zip_file = ZipFile(os.path.join(self.snap_dir,'%s.zip'%str(name)),'w')
            for file_path in file_paths:
                zip_file.write(
                    filename=file_path,
                    arcname=os.path.relpath(file_path,dir),
                    compress_type=ZIP_DEFLATED)
            if self.verbose:
                zip_file.printdir()
                print('\t> %s : '%name.ljust(15) + 'added')
            zip_file.close()
        # save snapshot config.json file 
        with open(os.path.join(self.snap_dir,'config.json'), 'w') as f:
            json.dump(self.config, f)

        # saves date,snap_dir and message meta data 
        with open(os.path.join(self.snap_dir,'meta.json'), 'w') as f:
            json.dump({
                "date" : self.date,
                "snap_dir" : self.snap_dir,
                "message" : self.message},f)

        static.snapshot_built(self.date)

    def retrieve(self):

        # make retrieve directory
        retrieve_dir = os.path.join(MAIN_DIR,self.date)
        if self.date not in os.listdir(MAIN_DIR):
            os.mkdir(retrieve_dir)

        # extract all zipfiles to retrieve directory
        for zip_filename in os.listdir(self.snap_dir):
            if '.zip' in zip_filename:
                if self.verbose:
                    print('> Unzipping: %s'%zip_filename)
                with ZipFile(os.path.join(self.snap_dir,zip_filename), 'r') as f:
                    f.extractall(os.path.join(retrieve_dir,zip_filename.replace('.zip','')))

        static.snapshot_retrieved(self.date)