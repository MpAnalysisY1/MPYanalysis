from optparse import OptionParser
from collections import Counter
import string,time,datetime
import os,math
import sys

starttime=datetime.datetime.now()
print(time.strftime("%y/%m/%d %H:%M:%S",time.localtime(time.time())))

parser=OptionParser()
parser.set_defaults(thread_number=5)
parser.set_defaults(Adapt='False')
parser.set_defaults(primerF='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
parser.set_defaults(primerR='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
parser.add_option("-I","--input_list", dest="info_list", help="Input your data information", metavar="LIST")
parser.add_option("-O","--outdir", dest="outdir", help="Output Directory", metavar="OUTDIR")
parser.add_option("-P","--threads", dest="thread_number", help="Input the thread number(default:5)", metavar="THREADS NUM")
parser.add_option("--AdaptClean", dest="Adapt", help="When set as True, built-in AdapterRemoval v2 (http://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-016-1900-2) is used to search for and remove remnant adapter sequences(default:False)", metavar="Boolean")
parser.add_option("-F","--PrimerForward", dest="primerF", help="Forward primer for cleaning, and --AdaptClean must be set as True.(default: Illumina TruSeq LT and TruSeq HT-based kits Read 1: AGATCGGAAGAGCACACGTCTGAACTCCAGTCA)", metavar="PrimerF")
parser.add_option("-R","--PrimerReverse", dest="primerR", help="Reverse primer for cleaning, and --AdaptClean must be set as True.(default: Illumina TruSeq LT and TruSeq HT-based kits Read 2: AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT)", metavar="PrimerR")
(options,args)=parser.parse_args()

thread_number=int(options.thread_number)

if not os.path.isdir(options.outdir):
    os.makedirs(options.outdir)
dir_path,file=os.path.split(os.path.abspath(sys.argv[0]))

find_SNP=os.path.join(dir_path,'scripts/find_SNP.py')
STRlen=os.path.join(dir_path,'scripts/STRlen.near30.string.mismach.rc.multiprocess.outseq.py')
STR_genotype=os.path.join(dir_path,'scripts/STR_genotype.py')
SNPref=os.path.join(dir_path,'reference/snp.near25.info.txt')
STRref=os.path.join(dir_path,'reference/STR.info.tab')
full_adapter=options.primerF+'NNNNNNNNNN'+options.primerR

magic_dict = {
    "\x1f\x8b\x08": "gz",
#    "\x42\x5a\x68": "bz2",
#    "\x50\x4b\x03\x04": "zip"
    }

max_len = max(len(x) for x in magic_dict)

def file_type(filename):
    with open(filename) as f:
        file_start = f.read(max_len)
    for magic, filetype in magic_dict.items():
        if file_start.startswith(magic):
            return filetype
    return "no match"

pfile=open(options.info_list,'r')
plines=pfile.read().split("\n")
for pline in plines[0:-1]:
    infos=pline.split("\t")
    sample=infos[0]
    reads_file=infos[1]
    os.system("rm -rf %s/%s" % (options.outdir,sample))
    os.system("mkdir -p %s/%s/01clean" % (options.outdir,sample))
    if options.Adapt == 'True':
        print(time.strftime("clean start at %y/%m/%d %H:%M:%S",time.localtime(time.time())))
        AdapterRemoval=os.path.join(dir_path,'tools/AdapterRemoval/adapterremoval-2.1.7/build/AdapterRemoval')
        if os.path.exists(AdapterRemoval):
            os.system("%s --file1 %s --adapter1 %s --trimns --trimqualities --minlength 50 --basename %s/%s/01clean/%s" % (AdapterRemoval,reads_file,full_adapter,options.outdir,sample,sample))
            os.system("mv %s/%s/01clean/%s.truncated %s/%s/01clean/%s_R1.clean.fq" % (options.outdir,sample,sample,options.outdir,sample,sample))
            print(time.strftime("clean done at %y/%m/%d %H:%M:%S",time.localtime(time.time())))
        else:
            print('ERROR: AdapterRemoval is not installed correctly !')
            break
    else:
        if file_type(reads_file) == 'gz':
            os.system("gzip -dc % > %s/%s/01clean/%s_R1.clean.fq" % (reads_file,options.outdir,sample,sample))
        else:
            os.system("mv % %s/%s/01clean/%s_R1.clean.fq" % (reads_file,options.outdir,sample,sample))
    print(time.strftime("uniq start at %y/%m/%d %H:%M:%S",time.localtime(time.time())))
    os.system("awk '{if(NR%%4 == 1){print \">\" substr($0, 2)}}{if(NR%%4 == 2){print}}' %s/%s/01clean/%s_R1.clean.fq > %s/%s/01clean/%s_R1.clean.fasta" % (options.outdir,sample,sample,options.outdir,sample,sample))
    os.system("cat %s/%s/01clean/%s_R1.clean.fasta | sort | uniq -c | awk '{if($1 > 5){print $1\"\t\"$2}}' | sort -nr -k1 > %s/%s/01clean/%s_R1_d5.reads" % (options.outdir,sample,sample,options.outdir,sample,sample))
    print(time.strftime("uniq end at %y/%m/%d %H:%M:%S",time.localtime(time.time())))
    print(time.strftime("genotype start at %y/%m/%d %H:%M:%S",time.localtime(time.time())))
    os.system("python %s -i %s -f %s/%s/01clean/%s_R1_d5.reads -o %s/%s/01clean/%s_R1_d5.reads.snp.gt.tab -p %s > %s/%s/01clean/%s_R1_d5.reads.snp.gt.log" % (find_SNP,SNPref,options.outdir,sample,sample,options.outdir,sample,sample,thread_number,options.outdir,sample,sample))
    os.system("python %s -i %s -f %s/%s/01clean/%s_R1_d5.reads -o %s/%s/01clean/%s_R1_d5.reads.rc.outseq.out -p %s > %s/%s/01clean/%s_R1_d5.reads.outseq.log" % (STRlen,STRref,options.outdir,sample,sample,options.outdir,sample,sample,thread_number,options.outdir,sample,sample))
    os.system("python %s -i %s/%s/01clean/%s_R1_d5.reads.rc.outseq.out -o %s/%s/01clean/%s_R1_d5.reads.rc.outseq.out.gt > %s/%s/01clean/%s_R1_d5.reads.rc.outseq.out.gt.log" % (STR_genotype,options.outdir,sample,sample,options.outdir,sample,sample,options.outdir,sample,sample))
    print(time.strftime("genotype end at %y/%m/%d %H:%M:%S",time.localtime(time.time())))

endtime=datetime.datetime.now()
print(time.strftime("%y/%m/%d %H:%M:%S",time.localtime(time.time())))
print("time used :",str(endtime-starttime))
