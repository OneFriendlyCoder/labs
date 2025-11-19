#!/bin/bash

# Save working directory to a tarball
cd ..
tar -zcvf working_directory.tar.gz working_directory/
rm -rf working_directory/