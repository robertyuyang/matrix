dir="srcxml"
mkdir $dir

function toxml(){

  f=$1
  srcML $f > ./$dir/$(dirname $f)/$(basename ${f%.*}).xml
}
function getdir(){
    for element in `ls $1`
    do  
        dir_or_file=$1"/"$element
        if [ -d $dir_or_file ]
        then 
            getdir $dir_or_file
        else
            echo $dir_or_file
	    subdir="./"$dir"/"$(dirname $dir_or_file)
	    echo $subdir
	    if [ ! -d $subdir ]; then
  	        mkdir -p $subdir
	    fi
	    toxml $dir_or_file $1
        fi  
    done
}
root_dir="src"
getdir $root_dir
