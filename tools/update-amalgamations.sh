#!/bin/bash

XUE_TOOL_DIR="$( cd "$( dirname ${BASH_SOURCE[0]} )" && pwd )"
XUE_ROOT_DIR="$( realpath "${XUE_TOOL_DIR}/../xue/" )"
AMALGAMATE_UTIL="${XUE_TOOL_DIR}/amalgamate-css.sh"
JSBUNDLE_UTIL="${XUE_TOOL_DIR}/bundle-js.sh"

CSS_BUNDLE_PATH="${XUE_ROOT_DIR}/static/xue/css/min"
JS_BUNDLE_PATH="${XUE_ROOT_DIR}/static/xue/js/bundle"

echo "CSS bundle will be stored in ${CSS_BUNDLE_PATH}"
echo " JS bundle will be stored in ${JS_BUNDLE_PATH}"


cd "${XUE_ROOT_DIR}"

cd static/xue/css
echo "Bundling CSS..."
"${AMALGAMATE_UTIL}" > "${CSS_BUNDLE_PATH}/amalgamation.css"

cd ie
echo "Bundling CSS for IE..."
"${AMALGAMATE_UTIL}" > "${CSS_BUNDLE_PATH}/ie-amalgamation.css"


cd "${XUE_ROOT_DIR}"

cd static/xue/js/framework
echo "Bundling JS frameworks..."
"${JSBUNDLE_UTIL}" > "${JS_BUNDLE_PATH}/framework.min.js"

cd ../ie/framework
echo "Bundling JS frameworks for IE..."
"${JSBUNDLE_UTIL}" > "${JS_BUNDLE_PATH}/ie-framework.min.js"


echo "all done"
