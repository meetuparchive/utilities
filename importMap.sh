#!/bin/sh

#Parameters: <command> 'mapurl' 'meetupurlname' 'time' 'key'
#time is in the form of milliseconds since the epoch

url=${1}



num=0
IFS=$'\n'

rm output.txt
curl --silent "$url" | iconv -f "UTF-8" -t "ISO-8859-1" > output.txt

#if the line does not contain a carrot, is lat lon info
for i in $(grep -v '>' output.txt | \
sed -n '1,$p' | \
sed -e 's/<georss:point>//' -e 's/<\/georss:point>//' | \
sed 's/^[ \t]*//'
)
do
	locs[$num]=$i
       	num=$(($num + 1))
done
num=0
#get stuff contained in title tags
for i in $(grep -E '(title>)' output.txt | \
sed -n '2,$p' | \
sed -e 's/<title>//' -e 's/<\/title>//' | \
sed 's/^[ \t]*//'
)
do
	titles[$num]=$i
       	num=$(($num + 1))
done
num=0
#get stuff contained in description tags
for i in $(grep -E '(description>)' output.txt | \
sed -n '2,$p' | \
sed -e 's/<description>//' -e 's/<\/description>//' -e 's/&nbsp;//g' | \
sed 's/^[ \t]*//'
)
do
	descs[$num]=$i
      	echo ${locs[$num]}
	x=`expr index "${locs[$num]}" " "`
	y=`expr $x - 1`
	d=${descs[${num}]##<*[}
	d=${d%%]*>}

	while [ `expr index "$d" "<"` -gt 0 ]
	do
		p=`expr index "$d" "<"`
		q=`expr index "$d" ">"`
		echo ${d}
		d="${d:0:p-1} ${d:q}"
	done
	t=${titles[${num}]}\ -\ ${d}
	curl -d "urlname=${2}&lat=${locs[${num}]:0:y}&lon=${locs[${num}]:x}&time=${3}&description=${t}&key=${4}&address1=" http://api.dev.meetup.com/ew/event/
       	num=$(($num + 1))
done

rm output.txt

