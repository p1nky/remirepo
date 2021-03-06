#!/bin/sh

name=phing
list=$(mktemp)

if [ -f $name-$1.tgz ]; then
	tar xif $name-$1.tgz
	tar tf $name-$1.tgz | sort >$list.old

	rm -r $name-$1/tasks/ext/jsmin

	sed -e '/^jsmin=/d' \
	    -i $name-$1/tasks/defaults.properties

	sed -En -e '/<ref name="jsmin"\/>/d; /<define name="jsmin">/,/<\/define>/d; 1h;1!H;${;g;s/<!--(\s|=)+JsMinTask(\s|=)+-->//;p;};' \
	    -i $name-$1/etc/phing-grammar.rng

	sed -e '/tasks\/ext\/jsmin/d' \
	    -e '/defaults.properties/s/md5sum.*name/name/' \
	    -e '/phing-grammar.rng/s/md5sum.*name/name/' \
	    -i package.xml

	tar czf $name-$1-strip.tgz package.xml $name-$1
	tar tf $name-$1-strip.tgz | grep -v '/$' | sort >$list.new

	diff -u $list.old $list.new
	rm -rf $name-$1 package.xml
else
	echo "usage $0 <version>"
fi
rm -f  $list*
