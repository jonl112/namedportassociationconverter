#new functionality: also converts text in clipboard from a module declaration into a module instatiation
#with named port association

##use with flag tb to convert a module into a dut

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
import pyperclip, sys

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


def convert_tb( str ):
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
            outstr += "." + s.strip() + "(" + "sim_" + s.strip() + "), "
        else:
            outstr += ","

    return pre + outstr.strip(" ").strip(",") + post

if (len(sys.argv)==1):
    f = pyperclip.paste().split("\n")
    toWrite = ""
    for line in f:
        if line == "\n":
            toWrite += line
        else:
            S = line.split("//")
            if len(S)==2:
                toWrite += convert(S[0]) + "//" + S[1] + "\n"
            else:
                toWrite += convert(line.strip("\n\t ")) + "\n"

    pyperclip.copy(toWrite);
elif ("tb" in str(sys.argv[1])):
    f = pyperclip.paste().split("\n")
    toWrite = ""
    for line in f:
        if ("module" in line):
            short = line[line.find(" ")+1:]
            bracket = short.split("(")
            toWrite += bracket[0] + " DUT(" + bracket[1] + "\n"

        elif line == "\n":
            toWrite += line
        else:
            S = line.split("//")
            if len(S)==2:
                toWrite += convert_tb(S[0]) + "//" + S[1] + "\n"
            else:
                toWrite += convert_tb(line.strip("\n\t ")) + "\n"

    pyperclip.copy(toWrite);

