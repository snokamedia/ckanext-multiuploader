# encoding: utf-8

from flask import request, url_for
import ckan.lib.helpers as h
from ckanext.multiuploader.lib import Helper
import ckan.plugins.toolkit as toolkit

class UploadController():

    def upload_resources():        
        if toolkit.g.user: 
            try:               
                package_name = request.form['pck_id']
                action = request.form['save']
                if action == "go-dataset":  # Previous button: go back to the dataset metadat                 
                    return h.url_for('dataset.edit', id=str(package_name) ,  _external=True)

                elif action == "go-dataset-complete": # Add resource to an active dataset
                    Helper.add_resource(package_name, request, False, int(request.form['isLink']))                
                    return h.url_for('dataset.read', id=str(package_name) ,  _external=True)
                
                else: # Add resource to a draft dataset
                    Helper.add_resource(package_name, request, True, int(request.form['isLink']))
                    if Helper.check_plugin_enabled("group_ownership"): # if group_ownership plugin exists:
                        return h.url_for('group_ownership.add_ownership_view', id=str(package_name) ,  _external=True)

                    elif Helper.check_plugin_enabled("media_wiki"): # if media_wiki plugin exists
                        return h.url_for('media_wiki.machines_view', id=str(package_name) ,  _external=True)

                    return h.url_for('dataset.read', id=str(package_name) ,  _external=True)
            except:
                return toolkit.abort(400, "missing data")


        else:
            return toolkit.abort(403, "You need to authenticate before accessing this function" )
    

    def cancel_dataset_plugin_is_enabled():
        if Helper.check_plugin_enabled('cancel_dataset_creation'):
            return True
        return False
