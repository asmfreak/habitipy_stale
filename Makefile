all: habitipy_stale/i18n/%/LC_MESSAGES/habitipy_stale.mo
.PRECIOUS: habitipy_stale/i18n/%.po.new
# scrape sources for messages
habitipy_stale/i18n/messages.pot: habitipy_stale/*.py
	xgettext --from-code utf-8  -L python -o $@ $^

# merge changes with previous translations
habitipy_stale/i18n/%.po.new: habitipy_stale/i18n/messages.pot habitipy_stale/i18n/%.po
	$(foreach f,$(filter-out $<,$^),msgmerge $f habitipy_stale/i18n/messages.pot > $(f).new;)

# compile runtime-usable messages
habitipy_stale/i18n/%/LC_MESSAGES/habitipy_stale.mo: habitipy_stale/i18n/%.po.new
	$(foreach f,$^,mkdir -p $(f:.po.new=)/LC_MESSAGES;)
	$(foreach f,$^,msgfmt -o $(f:.po.new=)/LC_MESSAGES/habitipy_stale.mo $(f);)

release:
	make tox
	make push
	make bump
	make tag
	make push
	make pypi

tox:
	tox

bump:
	bumpversion patch

tag:
	$(eval VERSION:=v$(shell bumpversion --dry-run --list patch | grep curr | sed -e 's/^.*=//g'))
	$(eval PREV_TAG:=$(shell git describe --tags --abbrev=0))
	(printf "Changes made in this version: \n"; git log $(PREV_TAG)..HEAD --graph --oneline --pretty="%h - %s") | git tag -F - -s $(VERSION)

push:
	git push
	git push --tags

pypi:
	python3 setup.py sdist upload --sign
#	python3 setup.py bdist_wheel upload --sign

clean_translation:
	rm -f habitipy_stale/i18n/*.new habitipy_stale/i18n/messages.pot

