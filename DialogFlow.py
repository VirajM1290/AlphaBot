# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:04:14 2018

@author: Monika Asawa
"""

import dialogflow_v2 as dialogflow
import re
from random import randint

project_id="alphabotagent"

entity_types_client = dialogflow.EntityTypesClient()

#Entity name may contain only the following: A-Z, a-z, 0-9, _ (underscore), - (dash). 
#And it should start with a letter."

def entity_name_validate_n_update(entityName):
    
    print("entity_name_validate_n_update method started")
    
    
    if re.search(r"^[a-zA-Z][[_|a-zA-Z|0-9|-]*]+",entityName):
        if re.search(r"(^\s)+",entityName):
            return entityName
        else:
            print("Validation failed 1")
            return "entityName_" + randint(100, 999)
    else:
        print("Validation failed 2")
        return "entityName_" + randint(100, 999)
    
    print("entity_name_validate_n_update method ended")
    

        
# Helper to get entity_type_id from display name.
def _get_entity_type_ids(display_name):
    
    print("_get_entity_type_ids method started")
    
    parent = entity_types_client.project_agent_path(project_id)
        
    entity_types = entity_types_client.list_entity_types(parent)
    entity_type_names = [
        entity_type.name for entity_type in entity_types
        if entity_type.display_name == display_name]

    entity_type_ids = [
        entity_type_name.split('/')[-1] for entity_type_name
        in entity_type_names]
    
    print("_get_entity_type_ids method ended")

    return entity_type_ids

def delete_entity_type(entity_type_id):
    """Delete entity type with the given entity type name."""

    print("delete_entity_type method started")
    
    try:
        entity_type_path = entity_types_client.entity_type_path(
            project_id, entity_type_id)
    
        entity_types_client.delete_entity_type(entity_type_path)
    
    except (dialogflow.api_core.exceptions) as error:
        return error

    print("delete_entity_type method ended")
        
def create_entity_type(display_name, kind):
    """Create an entity type with the given display name."""

    print("create_entity_type method started")
    
    kind = 'KIND_MAP'
    
    try:
    
        parent = entity_types_client.project_agent_path(project_id)
        
        display_name = entity_name_validate_n_update(display_name)
        
        entity_type = dialogflow.types.EntityType(
            display_name=display_name, kind=kind)
    
        response = entity_types_client.create_entity_type(parent, entity_type)
        
    except (dialogflow.api_core.exceptions) as error:
        return error
    
    print('Entity type created: \n{}'.format(response))
    print("create_entity_type method ended")    
    
def list_entity_types():
    
    print("list_entity_types method started")
    
    try:
    
        parent = entity_types_client.project_agent_path(project_id)
    
        entity_types = entity_types_client.list_entity_types(parent)
    
        for entity_type in entity_types:
            print('Entity type name: {}'.format(entity_type.name))
            print('Entity type display name: {}'.format(entity_type.display_name))
            print('Number of entities: {}\n'.format(len(entity_type.entities)))
    
    except (dialogflow.api_core.exceptions) as error:
        return error
    
    print("list_entity_types method ended")
            
def get_entity_displayNames():
    
    print("get_entity_displayNames method started")
    
    try:
        
        parent = entity_types_client.project_agent_path(project_id)
    
        entity_types = entity_types_client.list_entity_types(parent)
        
        entity_displayNames=[]
    
        for entity_type in entity_types:
            entity_displayNames.append(entity_type.display_name)    
        
    except (dialogflow.api_core.exceptions) as error:
        return error
    
    print("get_entity_displayNames method ended")
    
    return entity_displayNames

def delete_all_existing_entities():
    
    print("delete_all_existing_entities method started")
    
    try:
        
        entity_displayNames = get_entity_displayNames()
        
        for entityName in entity_displayNames:
            
            entity_type_ids = _get_entity_type_ids(entityName)
            
            for entity_type_id in entity_type_ids:
                
                delete_entity_type(entity_type_id)
                
    except (dialogflow.api_core.exceptions) as error:
        return error
    
    print("delete_all_existing_entities method ended")
            