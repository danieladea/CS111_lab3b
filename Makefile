###########################################
#NAME: Daniel Adea, Miles Wu
#EMAIL: dadea@ucla.edu, mileswu13@gmail.com
#ID: 204999515, 705192892
###########################################

default:
	echo 'python3 lab3b.py $$1' > lab3b
	chmod 777 lab3b

clean:
	rm -f lab3b *.tar.gz

dist: default
	tar -cvzf lab3b-204999515.tar.gz lab3b lab3b.py Makefile README
