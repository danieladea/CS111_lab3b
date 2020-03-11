#NAME: Daniel Adea
#EMAIL: dadea@ucla.edu
#ID: 204999515

default:lab3b.py
	rm -f lab3b
	ln -s lab3b.py lab3b
	chmod +x lab3b

clean:
	rm -f lab3b *.tar.gz

dist: default
	tar -cvzf lab3b-204999515.tar.gz lab3b.py Makefile README
