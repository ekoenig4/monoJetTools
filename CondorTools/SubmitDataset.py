import os
import sys
from multiprocessing import Process
import SubmitCondor
from dataset import getDataset
from argparse import ArgumentParser,ArgumentTypeError
labelmap = {
    'met':'METdata_','egamma':'EGdata_','singleele':'SEdata_','singlepho':'SPdata_',
    'zprime':'Zprime_','axial':'Axial_',
    'zjets':'Z','wjets':'W','dyjets':'DY','gjets':'GJets',
    'zjets_nlo':'ZNLO','wjets_nlo':'WNLO','dyjets_nlo':'DYNLO',
    'ewk':'','qcd':'QCD','st':'ST_','ttjets':'TTJets',
}
mclist = ['dyjets_nlo','dyjets','ewk','gjets','qcd','st','ttjets','wjets_nlo','wjets','zjets_nlo','zjets']
datalist = ['met','egamma','singleele','singlepho']
signalist = ['axial']
full_list = mclist + datalist

options = {
    'year':"",
    'region':"",
    'parallel':False,
    'batchsize':20,
    'submit':True,
    'data':True,
    'mc':True,
    'signal':True,
    'onlyWZG':False,
    'error':False,
    'verbose':False
}

for sample in full_list: options[sample] = False
def getargs():
    parser = ArgumentParser()
    def parse_bool(v):
        iv = int(v)
        if iv == 1: return True;
        if iv == 0: return False
        raise ArgumentTypeError("Input binary option")
    for key,value in options.iteritems():
        if type(value) == bool: parse_type = parse_bool
        else: parse_type = type(value)
        parser.add_argument("-"+key,default=value,type=parse_type)
    for key,value in vars(parser.parse_args()).iteritems():
        options[key] = value
def warning(prompt,data):
    if options['verbose']: print 'Warning submitting %s.' % data,prompt
def submit(data,sub=None,label=None,split=-1,filelist=True,script='analyze'):
    getargs()
    if not options['data'] and data in datalist:
        warning('Data is disabled',data); return
    if not options['mc'] and data in mclist:
        warning('MC is disabled',data); return
    if not options['signal'] and data in signalist:
        warning('Signal is disabled',data); return
    if options['onlyWZG'] and not any( wzg in data for wzg in ('wjets','zjets','dyjets','gjets')):
        warning('Only submitting WJets, ZJets, DYJets, or GJets enabled',data); return
    if any( options[sample] for sample in full_list ) and not options[data]:
        warning('Only submitting %s' % (', '.join([sample for sample in full_list if options[sample]]))); return
        
    SubmitCondor.NFILE_PER_BATCH = options['batchsize']
    SubmitCondor.DoSubmit = options['submit']
    SubmitCondor.ResubmitError = options['error']
    dataset = getDataset(data)
    if dataset == None: print '%s not found in dataset' % data; return
    if label is None: label = labelmap[data]
    subset = dataset[data]

    if sub is None: sublist = subset.keys()
    elif type(sub) != list: sublist = [sub]
    else: sublist = sub
    for sub in sublist:
        if sub not in subset: print '%s not found in subset' % sub; continue
        for i,input in enumerate(subset[sub]):
            clabel = '%s%s_%i' % (label,sub,i)
            nlabel = '%s%s_%i' % (labelmap[data],sub,i)
            command = [script,input,'post%s.root' % clabel,'-1','10000',nlabel,'split_%i' % split]
            if filelist: command = ['-f'] + command
            if any(options['region']): command = ['-r',options['region']] + command
            if any(options['year']): command = ['-y',options['year']] + command
            
            if options['parallel']:
                proc = Process(target=SubmitCondor.submit,args=(command,True))
                proc.start()
            else:
                SubmitCondor.submit( command )
    

