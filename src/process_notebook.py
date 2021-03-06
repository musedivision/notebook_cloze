import json
import re
import os
from functools import reduce
from copy import deepcopy

start_cloze_re = r'# cloze {'
end_cloze_re = r'# }'

def newCell(cell_type='code', execution_count=0,metadata={}, outputs=[], source=[] ):
        return { 'cell_type':cell_type, 'execution_count':execution_count, 'metadata':metadata, 'outputs':outputs, 'source':source }

def replaceHomePath(path): 
    docker_user_path = '/home/ubuntu'
    abs_p = os.path.abspath(path).split('/')[3:]
    return os.path.join(docker_user_path, '/'.join(abs_p))

def addModuleCell(path):
    lines = ['import sys \n', 'sys.path.insert(0, "%s") \n' % replaceHomePath(path)]
    return newCell(cell_type='code', source=lines)


def isCloze(txtArr, cloze_marker=r'cloze', checkEmpty=False):
    present = [re.search(cloze_marker,s) for s in txtArr]
    match = None
    if len(present):
        match = reduce(lambda c, acc: c if c else acc, present)
    
    if match is not None:
        return True
    else:
        return False

def extractCloze(cell_source):
    start_i = None
    end_i = None
    output = []
    for i, x in enumerate(cell_source):
        
        if isCloze([x], start_cloze_re):
            start_i = i 
        
        if start_i is not None and isCloze([x], end_cloze_re):
            end_i = i
            
            if not end_i - start_i == 1:
#                 print("EXTRACTING...")
                cloze_block = cell_source[start_i+1:end_i] # content of cloze tag
                sliced_source = cell_source[:start_i+1] + cell_source[end_i:] # includes cloze tag
                output.append((cloze_block, sliced_source))

            # reset detection
            start_i = None
            end_i = None
             
    
    return output


def readNotebook(path):
    # read file
    f = open(path, 'r')
    nb = f.read()
    nbd = json.loads(nb)
    
    module_path = os.path.dirname(os.path.abspath(path)) 
    
    cloze_blocks = []
    
    for i,c in enumerate(nbd['cells']):
        # go inside 1 cell
        # extract all cloze blocks
        if c['cell_type'] == 'code' and isCloze(c['source']):
            processed = extractCloze(c['source'])
            
            # add multiple clozes inside one cell
            for data in processed:
                clz_src, cln_src = data
                cloze_blocks.append({"i":i, "clz":clz_src, "cln_src":cln_src})
            
    output = []
    
    print('cloze_blocks: ', len(cloze_blocks))
    
    for clz in cloze_blocks:
        new_code_cells = deepcopy([c for c in nbd['cells']])
        new_code_cells[clz['i']]['source']=clz["cln_src"]
        new_nb = deepcopy({k:nbd[k] for k in nbd})
        new_code_cells.insert(0, addModuleCell(module_path))
        new_nb['cells'] = new_code_cells

        output.append((clz['clz'], new_nb))
    

    return output
