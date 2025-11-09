#!/bin/bash

cd ..
rm -rf working_directory/ 2>/dev/null
mkdir working_directory
tar -xvzf big_repo.tar.gz --directory working_directory/