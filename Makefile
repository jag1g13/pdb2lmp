.PHONY: clean
clean:
	rm *.ff *.data

.PHONY: test
test:
	py.test test/

.PHONY: check
check: test
