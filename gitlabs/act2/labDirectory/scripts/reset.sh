#!/bin/bash

# Reset file contents
rm -rf ../working_directory 2> /dev/null
mkdir ../working_directory
tar -zxvf big_repo.tar.gz --directory ../working_directory/