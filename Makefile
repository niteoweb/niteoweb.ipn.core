# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python
options =

all: tests

coverage: htmlcov/index.html

htmlcov/index.html: src/niteoweb/ipn/core/*.py src/niteoweb/ipn/core/tests/*.py bin/coverage
	@bin/coverage run --source=./src/niteoweb/ipn/core/ --branch bin/test
	@bin/coverage html -i --fail-under 99
	@touch $@
	@echo "Coverage report was generated at '$@'."

.installed.cfg: bin/buildout buildout.cfg buildout.d/*.cfg setup.py
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py
	@touch $@

$(python):
	virtualenv-$(version) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/flake8 src/niteoweb/ipn/core
	@for pt in `find src/niteoweb/ipn/core -name "*.pt"` ; do bin/zptlint $$pt; done
	@for xml in `find src/niteoweb/ipn/core -name "*.xml"` ; do bin/zptlint $$xml; done
	@for zcml in `find src/niteoweb/ipn/core -name "*.zcml"` ; do bin/zptlint $$zcml; done

clean:
	@rm -rf .installed.cfg bin parts develop-eggs htmlcov \
		src/niteoweb.ipn.core.egg-info lib include .Python

.PHONY: all tests clean
