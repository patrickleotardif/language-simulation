from random import *
from itertools import *
	
def newgrid(size):
	grid = []
	for i in range(1,size+1):
		row = []
		for j in range(1,size+1):
			row.append([])
		grid.append(row)
	return grid

def wsamp():
	import random
 	
	a = ['a','a','a', 'b','b','c' ,  ' ']
	i = 1
	word = []
 
	while True:

		letter = random.choice(a)
  
		if letter == ' ':
			if i == 1:
				while letter == ' ':
					letter = random.choice(a)
 
			else:
				break
 
		word.append(letter)
 
		i = i +1
 
	return ''.join(word)
	
def step(grid,i):
	x = randint(0,len(grid)-1)
	y = randint(0,len(grid)-1)
	
	agent = mset(grid[x][y])
	
	word = wsamp()
	while word in set(agent):
		word = wsamp()
	
	
	
	grid[x][y].append({"word": word,"marks": 0})
	
	#update_sur(grid,x,y)
	#update_all(grid)
	
	if i%100 == 0 :
		update_all(grid)

def update_sur(grid,x,y):
	change = False
	if x == 0:
		change = update_cell(grid,x+1,y) and change
	elif x == len(grid) - 1:
		change = update_cell(grid,x-1,y) and change
	else:
		change = update_cell(grid,x+1,y) and change
		change = update_cell(grid,x-1,y) and change

	if y == 0:
		change = update_cell(grid,x,y+1) and change
	elif y == len(grid) - 1:
		change = update_cell(grid,x,y-1) and change
	else:
		change = update_cell(grid,x,y+1) and change
		change = update_cell(grid,x,y-1) and change
	
	if change:
		update_sur(grid,x,y)	
	
def update_all(grid):
	for x in range(0,len(grid)):
		for y in range(0,len(grid)):
			update_cell(grid,x,y)

def mset(agent):
	s = set()
	if len(agent) > 0:
		for item in agent:
			s.add(item["word"])
	return s

def mlist(agent):
	l = []
	if len(agent) > 0:
		for item in agent:
			l.append(item["word"])
	return l

def format(set):
	l = []
	
	for item in set:
		d= {}
		d["marks"] = 0
		d["word"] = item
		l.append(d)
	
	return l
	
def update_cell(grid,x,y):

	sx = set()
	lx = []
	if x == 0:
		sx = mset(grid[x+1][y])
		lx = mlist(grid[x+1][y])
	elif x == len(grid) - 1:
		sx = mset(grid[x-1][y])
		lx = mlist(grid[x-1][y])
	else:
		sx = set.union(mset(grid[x+1][y]),mset(grid[x-1][y]))
		lx = mlist(grid[x+1][y]) + mlist(grid[x-1][y])
	
	sy = set()
	ly = []
	if y == 0:
		sy = mset(grid[x][y+1])
		ly = mlist(grid[x][y+1])
	elif y == len(grid) - 1:
		sy = mset(grid[x][y-1])
		ly = mlist(grid[x][y-1])
	else:
		sy = set.union(mset(grid[x][y+1]),mset(grid[x][y-1]))
		ly = mlist(grid[x][y+1]) + mlist(grid[x][y-1])
	
	l = ly + lx
	s = set.union(sx,sy)
	
	# union dict
	d= {}
	for item in s:
		d[item] = 0
	for item in l:
		d[item] = d[item] + 1
	
	tolerance = 2
	cand = set()
	#trim the union dict
	for word, freq in d.iteritems():
		if freq >= tolerance:
			cand.add(word)
	
	#add words kk fix this shit
	cand = cand.difference(mset(grid[x][y]))
	grid[x][y] = grid[x][y] + format(cand)
	
	#now add the marks
	mark = mset(grid[x][y]).difference(s)
	
	for item in grid[x][y]:
		if item["word"] in mark:
			item["marks"] = item["marks"] + 1
	

	max_marks = 200

	for item in grid[x][y]:
		if item["marks"] > max_marks:
			grid[x][y].remove(item)
	
	if len(cand) > 0:
		return True
	else:
		return False
	

def steps(grid,num,s):
	for i in range(1,num+1):
		step(grid,i)
		if (i%1000) == 0:
			s.append(lang_size(grid))
			print i

def exp_lang(lang):
	f = open('language.txt','w')
	
	for word,freq in lang.iteritems():
		f.write(str(len(word)) + '\t' + str(freq) + '\n')
	
	f.close()

def lang_size(grid):
	u = set()
	for agent in chain(*grid):
		u = set.union(u,mset(agent))
	d = dict()
	for word in u:
		d[word] = 0
	for agent in chain(*grid):
		for word in agent:
			d[word["word"]] = d[word["word"]] + 1
	
	#add in stuff that filters out a lot of the crap
	o = set()
	tolerance = 0.3
	
	for word, freq in d.iteritems():
		if freq > (tolerance*len(grid)*len(grid)):
			o.add(word)
			
	return len(o)
	
def lang(grid):
	u = set()
	for agent in chain(*grid):
		u = set.union(u,mset(agent))
	d = dict()
	for word in u:
		d[word] = 0
	for agent in chain(*grid):
		for word in agent:
			d[word["word"]] = d[word["word"]] + 1
	exp_lang(d)
	
	#add in stuff that filters out a lot of the crap
	o = set()
	tolerance = 0.3
	
	for word, freq in d.iteritems():
		if freq > (tolerance*len(grid)*len(grid)):
			o.add(word)
			
	return o

def newgridspin(size,num,s):

	grid = newgrid(size)
	steps(grid,num,s)
	return grid

def exp_vocab(vocab):
	f = open("vocab.txt","w")
	
	for item in vocab:
		f.write(str(item["len"]) + "\t" + str(item["voc"]) + "\n")
	
	f.close()

def vocab(grid,lang):	
	v= []
	for agent in chain(*grid):
		d = {}
		d["len"] = len(agent)
		d["voc"] = len(set.intersection(set(lang),mset(agent)))
		v.append(d)
	exp_vocab(v)
	return v

def exp_vgrid(vgrid):
	f = open("vgrid.txt","w")
	
	for row in vgrid:
		for item in row:			
			f.write(str(item) + "\t")
		f.write("\n")
	
	f.close()
	
def vgrid(grid,lang):
	v= []
	for row in grid:
		r = []
		for agent in row:
			r.append(len(set.intersection(set(lang),mset(agent))))
		v.append(r)
	
	exp_vgrid(v)
	
	return v

def exp_wgrid(wgrid):
	f = open("wgrid.txt","w")
	
	for row in wgrid:
		for item in row:			
			f.write(str(item) + "\t")
		f.write("\n")
	
	f.close()
	

def wgrid(grid,word):
	w= []
	for row in grid:
		r = []
		for agent in row:
			if word in mset(agent):
				r.append(1)
			else:
				r.append(0)
			
		w.append(r)
	
	exp_wgrid(w)
	
	return w
	
def analysis(g,s):
	l = lang(g)
	vocab(g,l)
	vgrid(g,l)
	
	f = open("growth.txt","w")
	
	for item in s:
		f.write(str(item) + "\n")
	
	f.close()
	
def do(size,steps):
	s= []
	g = newgridspin(size,steps,s)
	analysis(g,s)
	return g
	
 

 
 

