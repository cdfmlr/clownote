#!/bin/bash
# ❎未完成
cd /Users/c/clownote;

while [ -n "$1" ]; do
    case "$1" in 
        -n)
            file=`hexo new draft $2 | awk '{ print $NF }'`
            open $file
            shift
            ;;
        -p)
            hexo publish post $2
            hexo deploy --generate
            shift
            ;;
        *)
            echo "Unknown pramater:" $1
            shift
            ;;
    esac
    shift
done

cd -;