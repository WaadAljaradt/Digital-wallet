from graph import Graph
import sys

#read data from file and create initial graph
def pre_process(file_name):
	g = Graph()	
	try:
		with open(file_name,"rU") as f:
			next(f)
			for line in f :
				line = line.strip().split(",")[:5]
				l = len(line)
				if(l<5):
					print "Error : Missing values in the transaction"
					quit()
				else:
					g.add_vertex(line[1].lstrip().strip())
					g.add_edge(line[1].lstrip().strip(),line[2].lstrip().strip())
		return g
	except IOError:
		print "File doesnt Exists "+file_ame
		quit()
#process stream data			
def process_stream(file_name,g):
	feature_1 =[]
	feature_2 =[]
	feature_3 =[]
	i = 0
	trust = "trusted"
	unverified = "unverified"
	with open(file_name,"rU") as f:
		next(f)
		for transaction in f :
			transaction = transaction.strip().split(",")[:5]
			l = len(transaction)
			if(l<5):
				print "Error : Missing values in the transaction"
				continue
			else:
				root= transaction[1].lstrip().strip()
				end = transaction[2].lstrip().strip()
				FOUND = False
				level=0
				#check frist two levels
				result= find_level_BSF(root,end,g)
				if result[0]!= False:
					FOUND = True
					level = result[1]
					#feature 1 output 
					if level == 1 :
						feature_1.append(trust)
						feature_2.append(trust)
						feature_3.append(trust)
 
					#feature 2 output 
					elif level == 2 :
						feature_1.append(unverified)
						feature_2.append(trust)
						feature_3.append(trust)

				#check deeper to 3 and levels
				else:
					degree_3= check_level(result[1],end,g,3)
					if degree_3[0] != False:
						FOUND = True	
					else:
						degree_4 = check_level(degree_3[1],end,g,4)
						if degree_4[0] != False:
							FOUND = True	
					if FOUND :
						feature_1.append(unverified)
						feature_2.append(unverified)
						feature_3.append(trust)
			if not FOUND:
				feature_1.append(unverified)
				feature_2.append(unverified)
				feature_3.append(unverified)
			i+=1
	f.close()						
	return (feature_1,feature_2,feature_3)

#check_level 3 and 4 

def check_level(edges,end,g,level):
	visited ={}
	degree_4 =[]
	for edge in edges:
		for child in g.edges(edge) :
				if child in visited :
					continue
				if child == end:
					return (True,level+1)
				if level == 3:
					degree_4.append(child)
				visited[child]=True
	return False,degree_4
					 
# BSF within 2 length path
def find_level_BSF(root, end,g):
	if root == end :
		return (True,0)
	level =0
	result = {}
	visited = {}
	visited[root] = True
	list =[]
	list.append(root)
	result[level] = list
	feature3_cache =[]			
	while (level < 2):
		list = []
		l = len(result[level])
		for i in range(0,l):
			n = result[level][i]
			if n == end:
				return (True,level)
			for edge in g.edges(n) :
				if edge in visited :
					continue 
				if edge == end:
					return (True,level+1)
				if (level+1) == 2 :
					feature3_cache.append(edge)
				list.append(edge)
				visited[edge]= True
		if len(list) > 0 :
			result[level+1]=list
			level = level+1
		else:
			break
			
	return False,feature3_cache 

def output_results(files,result):
	for file, out in zip(files, result):
		f=open(file,'w+')
		o='\n'.join(out)
		f.write(o)
		f.close()
		
def ____main___():
	args = sys.argv
	#read args
	data_file = args[1]
	test_file = args[2]
	#prepare initial graph args
	g = pre_process(data_file)
	print("INFO : Done_reading_data")
	print("INFO : Done_create_graph")
	output = process_stream(test_file,g)
	print("INFO : Done_processing_test")
	#output to files
	output_results(args[3:6],output)
	
____main___()	

	


