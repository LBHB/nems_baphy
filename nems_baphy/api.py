import os
import io
import re

from flask import abort, Response, request
from flask_restful import Resource

from nems_baphy.access import load_recording_from_baphy
import nems_baphy.db as nd
import nems_db.baphy as baphy

# Define some regexes for sanitizing inputs
RECORDING_REGEX = re.compile(r"[\-_a-zA-Z0-9]+\.tar\.gz$")
CELLID_REGEX = re.compile(r"^[\-_a-zA-Z0-9]+$")
BATCH_REGEX = re.compile(r"^\d+$")


def valid_recording_filename(recording_filename):
    ''' Input Sanitizer.  True iff the filename has a valid format. '''
    matches = RECORDING_REGEX.match(recording_filename)
    return matches


def valid_cellid(cellid):
    ''' Input Sanitizer.  True iff the cellid has a valid format. '''
    matches = CELLID_REGEX.match(cellid)
    return matches


def valid_batch(batch):
    ''' Input Sanitizer.  True iff the batch has a valid format. '''
    matches = BATCH_REGEX.match(batch)
    return matches


def ensure_valid_cellid(cellid):
    if not valid_cellid(cellid):
        abort(400, 'Invalid cellid:' + cellid)


def ensure_valid_batch(batch):
    if not valid_batch(batch):
        abort(400, 'Invalid batch:' + batch)


def ensure_valid_recording_filename(rec):
    if not valid_recording_filename(rec):
        abort(400, 'Invalid recording:' + rec)


def not_found():
    abort(404, "Resource not found. ")


class BaphyInterface(Resource):
    '''
    An interface to BAPHY that returns NEMS-compatable signal objects
    '''
    def __init__(self, **kwargs):
        # self.host = kwargs['host'],
        # self.port = kwargs['port'],
        # self.user = kwargs['user'],
        # self.pass = kwargs['pass'],
        # self.db = kwargs['db']
        # self.db = ... # TODO: Connect to database HERE
        pass

    def get(self, batch, cellid):
        '''
        Queries the MySQL database, finds the file, and returns
        the corresponding data in a NEMS-friendly Recording object.
        '''
        ensure_valid_batch(batch)
        ensure_valid_cellid(cellid)
        batch = int(batch)

        options = request.args.copy()
        
        # TODO: Sanitize optional arguments
        #if 'rasterfs' in request.args:
        #    options['rasterfs'] =  int(request.args['rasterfs'])
        #if 'chancount' in request.args:
        #    options['chancount'] =  int(request.args['chancount'])
        # TODO: stimfmt is a string, includprestim/stim/pupil are booleans
        rec = baphy.baphy_load_recording(cellid, batch, options)
        #rec = load_recording_from_baphy(batch=batch, cellid=cellid, **options)
        if rec:
            targz = rec.as_targz()
            return Response(targz, status=200, mimetype='application/gzip')
        else:
            abort(400, 'load_recording_from_baphy returned None')

    def put(self, batch, cellid):
        abort(400, 'Not yet implemented')

    def delete(self, batch, cellid):
        abort(400, 'Not yet Implemented')


class DirectoryInterface(Resource):
    '''
    An interface that serves out NEMS-compatable .tar.gz recordings
    '''
    def __init__(self, **kwargs):
        self.targz_dir = kwargs['targz_dir']

    def get(self, rec):
        '''
        Serves out a recording file in .tar.gz format.
        TODO: Replace with flask file server or NGINX
        '''
        ensure_valid_recording_filename(rec)
        filepath = os.path.join(self.targz_dir, rec)
        if not os.path.exists(filepath):
            not_found()
        d = io.BytesIO()
        with open(filepath, 'rb') as f:
            d.write(f.read())
            d.seek(0)
        return Response(d, status=200, mimetype='application/gzip')

    def put(self, rec):
        abort(400, 'Not yet implemented')

    def post(self, rec):
        abort(400, 'Not yet implemented')

    def delete(self, rec):
        abort(400, 'Not yet Implemented')
