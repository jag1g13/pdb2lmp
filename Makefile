.PHONY: clean
clean:
	rm *.ff *.data | true

.PHONY: test
test:
	py.test test/

.PHONY: check
check: test
