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

ARCHIVE_DIR="pages/archive/"

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
        \"id\":\"$3\",\
        \"src\":\"$2\",\
        \"user\":\"%an\",\
        \"comment\":\"%s\",\
        \"created\":\"%ai\"\
    }" $1
}

function print_front_matter {
    printf "%s\nlayout: page\npermalink: %s\n%s\n\
<style>html{margin-top: 27px}</style>\
<div class=\"hist\">version: %s.\
    <a href=\"/digitalcitizens/about/\">back to latest</a>\
</div>\n\n\
<h1 class=\"post-title\">About</h1>" "---" $1 "---" $2
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
    # INDEX_OUT=$(printf %03d $INDEX)
    OUTNAME=$(basename -- "$FILENAME")
    OUT_FILEPATH="pages/archive/$HASH.$OUTNAME"
    ID_STR=$(basename -- "$OUT_FILEPATH")
    WEB_PATH="$OUT_FILEPATH.html"
    # create the history file.
    echo "Making file: $OUT_FILEPATH from commit $HASH:$FILENAME"

    print_front_matter $WEB_PATH $ID_STR > $OUT_FILEPATH
    git show "$HASH:$FILENAME" | awk 'NR>5' >> $OUT_FILEPATH

    # build up json history string.

    ROW=$(git_log_message_to_json $HASH $WEB_PATH $ID_STR)
    HIST_CONTENTS="$HIST_CONTENTS $ROW"
    let INDEX++
done

# write the commit meta data to a nicely formated json
echo "$HIST_CONTENTS ]" | python -m json.tool > _data/history.json