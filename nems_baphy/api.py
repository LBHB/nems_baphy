import re
from flask import abort, Response, request
from flask_restful import Resource

import nems_baphy.baphy as baphy

# Define some regexes for sanitizing inputs
CELLID_REGEX = re.compile(r"^[\-_a-zA-Z0-9]+$")
BATCH_REGEX = re.compile(r"^\d+$")


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


def valid_boolean(name, val):
    if request.args['pupil'] == 'True':
        return True
    elif request.args['pupil'] == 'False':
        return False
    else:
        abort(400, '{} must be True or False'.format(name))


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
        # self.db = ... # TODO: Connect to database HERE, not in db.py
        pass

    def get(self, batch, cellid):
        '''
        Queries the MySQL database, finds the file, and returns
        the corresponding data in a NEMS-friendly Recording object.
        '''
        ensure_valid_batch(batch)
        ensure_valid_cellid(cellid)
        batch = int(batch)

        options = {}
        if 'rasterfs' in request.args:
            options['rasterfs'] = int(request.args['rasterfs'])

        if 'chancount' in request.args:
            options['chancount'] = int(request.args['chancount'])

        if 'pupil' in request.args:
            options['pupil'] = valid_boolean('pupil', request.args['pupil'])

        if 'stim' in request.args:
            options['stim'] = valid_boolean('stim', request.args['stim'])

        if 'includeprestim' in request.args:
            options['includeprestim'] = valid_boolean('includeprestim', request.args['includeprestim'])

        if 'stimfmt' in request.args:
            options['stimfmt'] = request.args['stimfmt']

        # TODO: Add other allowed options as needed

        rec = baphy.baphy_load_recording(cellid, batch, options)

        if rec:
            targz = rec.as_targz()
            return Response(targz, status=200,
                            mimetype='application/x-tgz')
        else:
            abort(400, 'load_recording_from_baphy returned None')

    def put(self, batch, cellid):
        abort(400, 'Not implemented; use PUT instead')

    def delete(self, batch, cellid):
        abort(400, 'Not implemented; allowing http DELETE is a little dangerous.')
