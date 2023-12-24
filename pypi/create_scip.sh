# npm install -g @sourcegraph/scip-python
# npm install @sourcegraph/scip-python                                           

export PROJECT_NAME=a10_octavia
export EMBEDDING_DATA_DIR=embeddings
export TARGET_DIR=downloads/a10-octavia-2.2.0/a10_octavia

node node_modules/@sourcegraph/scip-python/dist/scip-python.js index --project-name $PROJECT_NAME --output $EMBEDDING_DATA_DIR/$PROJECT_NAME.scip --target-only $TARGET_DIR