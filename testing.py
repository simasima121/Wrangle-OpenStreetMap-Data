import re
val = ['SW18', '4TF', 'sim']
postcode = ['57643']


#tested = ['Rectory', 'Grove', 'Hampton', 'TW12', '1EG']
tested = ['Park', 'Road,', 'N8', '8TE']

node = {'created':{}, 'address':{}}

count = 0
found = []
not_found = []
for i in range(len(tested)):
    try:
        if re.search(r'.*\d', tested[i]):
            print tested[i], tested
            found.append(tested[i])
            count += 1
        else:
        	not_found.append(tested[i])

        if count > 1 and i == len(tested)-1:
            print count, i, len(tested)
            print "found: ", found
            s = ' '.join(found)
            print "joined found: ", s
            node['address']['postcode'] = s
            if not_found:
            	s = ' '.join(not_found)
            	node['address']['street'] = s
            print "postcode: ", node['address']['postcode']
            print "street: ", node['address']['street']
            
        elif i == len(tested)-1 and count < 2:
            print tested
            for v in tested:
            	print v
            #node['address']['street'] = 
    except:
        node['address'][kval] = vval
print node     



    

"""
for v in val:
	try:
		print v
		print re.search(r'.*\d', v)
	except:
		print re.match(r'\d', v)

for p in postcode:
	print re.search(r'^\d{5}$', p).group()
"""