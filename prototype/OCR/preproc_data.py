import re

def preprocessing(file):
    text=""
    substring1 = " et "
    substring2 = " ou "


    with open(file,'r') as f:

        
        for line in f:
            if len(line)>10:
                #new line when encounter a coma which is not attached to a number
                index = 1
                pos_virg = [m.start() for m in re.finditer(',', line)]

                for pos in pos_virg:
                    try:
                        int(line[pos-1])
                    except:
                        line = line[:pos+index] + '\n' + line[pos+index:]
                        index+=1
        

                #new line when encounter a "et"
                try:
                    a = line.index(substring1)
                    line = line[:a] + '\n' + line[a:]
                except ValueError:
                    pass
                #new line when encounter a "ou"
                try:
                    a = line.index(substring2)
                    line = line[:a] + '\n' + line[a:]
                except ValueError:
                    pass
                #new line when encounter a "+"
                try:
                    a = line.index("+")
                    line = line[:a] + '\n' + line[a:]
                except ValueError:
                    pass
                
                #changes the "I" in ones, google vision often confuse the issue
                line = line.replace("I","1")

                # new line when encounter a point
                # try:
                #     a = line.index(".")
                #     line = line[:a] + '\n' + line[a:]
                # except ValueError:
                #     pass
            
                # new line when encounter a ":"
                # try:
                #     a = line.index(":")
                #     line = line[:a] + '\n' + line[a:]
                # except ValueError:
                #     pass
                
                text+=line
        f.close()

    with open(file,'w') as f:

        f.write(text)
        f.close()