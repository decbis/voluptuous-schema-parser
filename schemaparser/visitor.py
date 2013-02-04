import ast
from _ast import Call, Attribute, Name
from _ast import List, Tuple, Dict, Num, Str
from schemaparser.constants import *
from schemaparser.entity import *

class SchemaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.entities = []
        self._required = False
        self._extra = False

    def _get_node_name(self, node):
        if isinstance(node.func, Name):
            return node.func.id

        if isinstance(node.func, Attribute):
            return node.func.attr

    def _is_schema_node(self, node):
        if isinstance(node.func, Name) or isinstance(node.func, Attribute):
            return self._get_node_name(node) == SCHEMA_CLASS

        return False

    def _get_schema_kwargs(self, args, keywords):
        kwargs = dict(zip(SCHEMA_PARAMS, SCHEMA_PARAMS_VALUES))
        for keyword in keywords:
            kwargs[keyword.arg] = keyword.value.id
        for idx, arg in enumerate(args):
            kwargs[SCHEMA_PARAMS[idx]] = arg

        return kwargs

    def _get_call_args(self, args, keywords):
        call_args = []
        #for keyword in keywords:
        #    node = keyword.value
        #    if isinstance(node, Call):
        #        inner_call_args = self._get_call_args(node.args, node.keywords)
        #        call_args.append(inner_call_args)
        #    else:
        #        call_args.append(node.id)
        
        for arg in args:
            node = arg
            if isinstance(node, Call):
                inner_call_args = self._get_call_args(node.args, node.keywords)
                func_name = self._get_node_name(node)
                call_args.append([func_name ,inner_call_args])
            if isinstance(node, Name):
                call_args.append(node.id)
            if isinstance(node, Num):
                call_args.append(node.n)
            if isinstance(node, Str):
                call_args.append(node.s)
        
        return call_args

    def _parse_key(self, key):
        if isinstance(key, Str):
            return get_key_dict(key.s, self._required)

    def _parse_requirements(self, value, current_requirements):
        if isinstance(value, Name):
            current_requirements.append([value.id, []])
        if isinstance(value, Call):
            func_name = self._get_node_name(value)
            call_args = self._get_call_args(value.args, value.keywords)
            current_requirements.append([func_name, call_args])
        
        return current_requirements

    def _parse_value(self, value):
        return get_value_dict(self._parse_requirements(value, []))   
    
    def _parse_dict(self, schema_dict):
        keys = schema_dict.keys
        values = schema_dict.values
        
        entity = []
        for idx, key in enumerate(keys):
            entity.append(get_field_dict(self._parse_key(key),
                                         self._parse_value(values[idx])))
        return entity

    def _parse_func_any(self, func):
        pass

    def _parse_func_all(self, func):
        pass

    def visit_Call(self, node):
        # looking for the Schema creation call
        if self._is_schema_node(node):
            kwargs = self._get_schema_kwargs(node.args, node.keywords)
            self._required = kwargs["required"]
            self._extra = kwargs["extra"]
            
            schema = kwargs["schema"]
            
            if isinstance(schema, Dict):
                self.entities.append(self._parse_dict(schema))
