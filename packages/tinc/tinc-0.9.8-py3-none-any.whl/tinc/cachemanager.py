# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:32:03 2020

@author: Andres
"""

import json
import os
import jsonschema

from typing import NamedTuple, List

# C++ cache structs - they are used as NamedTuple here
class UserInfo(NamedTuple):
    user_name: str
    user_hash: str
    ip: str
    port: int
    server: bool

# struct SourceArgument {
#   std::string id;
#   VariantValue value;
# };

class SourceArgument(NamedTuple):
    id: str
    value: any

# struct FileDependency {
#   DistributedPath file;
#   std::string modified;
#   uint64_t size;
# };

class FileDependency(NamedTuple):
    file: str
    modified: str
    size: int

# struct SourceInfo {
#   std::string type;
#   std::string
#       tincId; // TODO add heuristics to match source even if id has changed.
#   std::string commandLineArguments;
#   DistributedPath workingPath{""};
#   std::string hash;
#   std::vector<SourceArgument> arguments;
#   std::vector<SourceArgument> dependencies;
#   std::vector<FileDependency> fileDependencies;
# };

class SourceInfo(NamedTuple):
    type: str
    tinc_id: str
    command_line_arguments: str
    working_path: str
    hash: str
    arguments: List[SourceArgument]
    dependencies: List[SourceArgument]
    file_dependencies: List[FileDependency]

# struct CacheEntry {
#   std::string timestampStart;
#   std::string timestampEnd;
#   std::vector<std::string> filenames;
#   UserInfo userInfo;
#   SourceInfo sourceInfo;
#   uint64_t cacheHits{0};
#   bool stale{false};
# };

class CacheEntry(NamedTuple):
    timestamp_start: str
    timestamp_end: str
    filenames: List[str]
    user_info: UserInfo
    source_info: SourceInfo
    hash: str
    arguments: List[SourceArgument]
    dependencies: List[SourceArgument]
    file_dependencies: List[FileDependency]

# FIXME use more robust cache metadata defined in the metadata schema


class CacheManager(object):
    def __init__(self, directory = "python_cache"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._cache_dir = directory
        self._validator = None
        # with open("tinc_cache_schema.json") as f:
        #     schema = json.load(f)
        #     self._validator = jsonschema.Draft7Validator(schema)

    def append_entry(self, entry):
        pass

    def entries(self):
        pass

    def find_cache(self,source_info, verify_hash = True):
        pass

    def clear_cache(self):
        print("Not implemented yet")

    '''
    Get full cache path
    '''
    def cache_directory(self):
        pass

    def update_from_disk(self):
        pass

    def write_to_disk(self):
        pass

    def dump(self):
        #print json metadata
        pass

            
    def construct_filename(self, args):
        # TODO allow setting filename template.
        filename = self._cache_dir + '/cache_'
        # TODO more robust checks for arguments and source process
        for param_id, value in args.items():
            filename += f'{value}_'
        filename = filename[:-1]
        return filename
        
    def store_cache(self, data, args):
        with open(self.construct_filename(args), 'w') as fp:
            json.dump(data, fp)
            print(f"stored cache: {self.construct_filename(args)}")
    
    def load_cache(self, args):
        data = None
        filename = self.construct_filename(args)
        if os.path.exists(filename):
            with open(filename) as fp:
                data = json.load(fp)
                
                print(f"loaded cache: {filename}")
        return data
    
    def remove_cache_file(self, args):
        
        filename = self.construct_filename(args)
        if os.path.exists(filename):
            print(f"removing {filename}")
            os.remove(filename)


if __name__ == "__main__":
    c = CacheManager()
    #print(c._validator)