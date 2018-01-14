#new functionality: also converts text in clipboard from a module declaration into a module instatiation
#with named port association

#this script converts an implicitly defined port association into named port assocation syntax
#for example: example dut(ain, bin, cout) ==> example dut(.ain(ain), .bin(bin), .cout(cout))
#also handles line comments for example:
'''example dut (//inputs
                ain, bin,
                //outputs
                cout
                );
    into

    example dut(//inputs
                .ain(ain), .bin(bin),
                //outputs
                .cout(cout)
                );
'''
import pyperclip

def convert( str ):
    if str =="":
        return str
    outstr = ""
    pre = ""
    post = ""
    S = str.split("(")
    str = S[-1]
    if len(S)==2:
        pre = S[0] +"("
    elif len(S)!=1:
        return "wtf"
    S = str.split(")")
    str = S[0]
    if len(S)==2:
        post = ")" + S[1]
    elif len(S)!=1:
        return "wtf"
    S = str.split(",")
    outstr = ""
    for s in S:
        if s.strip():
            outstr += "." + s.strip() + "(" + s.strip() + "), "
        else:
            outstr += ","

    return pre + outstr.strip(" ").strip(",") + post

pyperclip.copy(convert(pyperclip.paste()));



f = open ("data.txt", "r")
toWrite = ""

for line in f:
    if line == "\n":
        toWrite += line
    else:
        S = line.split("//")
        if len(S)==2:
            toWrite += convert(S[0]) + "//" + S[1]
        else:
            toWrite += convert(line.strip("\n\t ")) + "\n"

f.close()

f = open ("data.txt","w")
f.write(toWrite)
f.close()
