import subprocess as sp
    # Using "from multiprocessing import Process" lets you just type "Process" into the splitJobs Function below, 
        # if you were to just type "import multiprocessing", you would have to type "multiprocessing.Process(...)" in
        # the function instead.
from multiprocessing import Process
from pyfaidx import Fasta

### SPLICE FUNCTION
    # This function will take the Fasta file and do the following:
    #       1. Puts all items that do not start with "NC" (AKA all contigs) into a list called "contigKeys"
    #       2. contigKeys will then be split up into lists with a size of the desired run size
    #       3. All of the lists will then be put into a list, and this is returned
def splice(fastaLoc, size):
    fasta = Fasta(fastaLoc)
    
    # 1
    contigKeys = []
    for contig in fasta.keys():
        if contig.startswith('NC'):
            continue
        contigKeys.append(contig)

    # 2 & 3
    return [contigKeys[i:int(i+size)] for i in range(0, len(contigKeys), int(size))]


### MAKE FILE FUNCTION
    # For each of the contigs in the list provided, a file will be made within a desired directory.
    # The name of each file will be the name of each contig.
def makeFile(contig, contigKeyFileDest):
    sp.call(["touch", contigKeyFileDest + "/" + contig])


### SPLIT JOBS FUNCTION
    # 1. The function starts off by using the SPLICE Function and saving the lists of lists into a variable called "scopes".
    #       Remember: Each of the lists' lengths within "scopes" are equal to the run size you inputted
    # 2. A directory is then made with your desired name in your desired location.
    # 3. Now... (here comes the multiprocessing magic)
    #       For each of the lists within the "scopes" list, we are going to tell the computer to run the contigs within 
    #           each list, simultaneously. For example, if each list within "scopes" contains a list of length 5, then 5 
    #           contigs will run at once, and then the next group will run together, and so on.
    #       A. To do this, we must create a new list (AKA "jobs") with our scopes's lists + each of the list's contigs and their 
    #           commands. For example, if our scope is currently [A,B,C], then the altered list (AKA "jobs") 
    #           will be [do(A), do(B), do(C)]. We have to make a new list of "scopes" and not alter the current one. It's 
    #           simpler.
    #       B. Once we have successfully copied over the "jobs" list with all of the inner lists' contigs + the contigs' commands, 
    #           now we run it. Since it is a for-loop, we're going to run each of the scopes sequentially, and the n-number
    #           of items within each scope will run together.
    #       
def splitJobs(size, fastaLoc, contigKeyFileLoc, fileName):
    # 1
    scopes = splice(fastaLoc, size)

    # 2
    sp.run(["mkdir", contigKeyFileLoc + "/" + fileName])

    # 3A
    jobs = []
    for scope in scopes:
        for contig in scope:
            j = Process(target=makeFile, args=(contig, contigKeyFileLoc + "/" + fileName))
            jobs.append(j)
            j.start()

        i = 0
        for j in jobs:
            j.join()
            i += 1

        del jobs[:]

        

if __name__ == "__main__":
    splitJobs(22, '/Users/laurengsabo/Documents/mcgrath/2023/GCF_000238955.4_M_zebra_UMD2a_genomic.fna', "/Users/laurengsabo/Documents/mcgrath/2023/VSCode", "contigTrash")