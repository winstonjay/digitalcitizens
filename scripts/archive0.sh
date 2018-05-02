# archive1.sh:
#
set -e

# check we have enough args to satisfy the program
# about page default: _site/about/index.html
if [ $# == 0 ]
then
    echo "No Args. Filename needed."
    exit
fi

FILENAME="$1"

# check if the filename provided exists.
if [ ! -f $FILENAME ]
then
    echo "File: $FILENAME not found!"
    exit
fi

ARCHIVE_DIR="pages/archive/pages"

if [ ! -d $ARCHIVE_DIR ]
then
    echo "Creating dir: $ARCHIVE_DIR"
    mkdir $ARCHIVE_DIR
fi

# check if we are in the root of our git directory.
ROOT_FOLDER=$(git rev-parse --show-toplevel)
CURR_DIR=$(pwd)
if [ "$ROOT_FOLDER" != "$CURR_DIR" ]
then
  echo "Switch to the root of the repo and try again. Should be in $ROOT_FOLDER"
  exit
fi

# return commit
function git_log_short {
    git log --oneline --decorate $*
}

function get_col {
    awk -v col=$* '{print $col}'
}

function git_log_message_to_json {
    git log -1 --pretty=format:"{\
        \"filename\":\"$2\",\
        \"user\":\"%an\",\
        \"comment\":\"%s\",\
        \"created\":\"%ai\"\
    }" $1
}

HASHES=$(git_log_short $FILENAME | get_col 1)
HIST_CONTENTS="["
INDEX=1

for HASH in $HASHES
do
    if [ $INDEX != 1 ]
    then
        HIST_CONTENTS="$HIST_CONTENTS, "
    fi
    INDEX_OUT=$(printf %03d $INDEX)
    OUT_FILEPATH="archive/$FILENAME.$INDEX_OUT.$HASH"

    # create the history file.
    echo "Making file: $OUT_FILEPATH from commit $HASH:$FILENAME"
    git show $HASH:$FILENAME > $OUT_FILEPATH

    # build up json history string.
    ROW=$(git_log_message_to_json $HASH $OUT_FILEPATH)
    HIST_CONTENTS="$HIST_CONTENTS $ROW"
    let INDEX++
done

# write the commit meta data to a nicely formated json
echo "$HIST_CONTENTS ]" | python -m json.tool > assets/history.json