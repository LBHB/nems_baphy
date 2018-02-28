import os
import io
import re

from flask import abort, request, Response
from flask_restful import Resource

# Define some regexes for sanitizing inputs
RECORDING_REGEX = re.compile(r"[\-_a-zA-Z0-9]+\.tar\.gz$")
CELLID_REGEX = re.compile(r"^\w+\d+\w-\w\d$")  # gus018c-a3
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
        print(kwargs['host'],
              kwargs['port'],
              kwargs['user'],
              kwargs['pass'],
              kwargs['db'])
        # self.db = ... # TODO

    def get(self, batch, cellid):
        '''
        Queries the MySQL database, finds the file, and returns
        the corresponding data in a NEMS-friendly Recording object.
        '''
        ensure_valid_batch(batch)
        ensure_valid_cellid(cellid)

        # Query MySQL to get a list of files
        # TODO

        # Check that the files exist. If any are missing, throw an error
        # TODO
        # for f in files:
        #     if not os.exists(f):
        #        not_found()

        # Now convert all files into a Recording object
        # TODO
        # rec = convert_to_rec()

        # Zip the recording object
        # TODO
        d = '{"msg": "batch and cellid are sanitized"}'
        
        return Response(d, status=200, mimetype='application/json')

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
