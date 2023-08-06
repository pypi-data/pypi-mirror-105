#!/usr/bin/python3
""" Python module for opinied command line processing of OWL ontologies"""

__version__ = "0.1.3"

from jjcli import *
from unidecode import unidecode
import json
import owlrl
from   owlrl import convert_graph, RDFXML, TURTLE, JSON, AUTO, RDFA
import rdflib
from   rdflib.namespace import RDF, OWL, RDFS, SKOS, FOAF

def best_name_d(g : rdflib.Graph) -> dict :
   """ FIXME: IRIRef -> str based on RDFS.label, id, ??? """
   bestname={}
   for n in g.all_nodes():
       if islit(n): continue
       if name := g.preferredLabel(n) :
           bestname[s]=name[0].strip()
       else:
           txt = term.n3(g.namespace_manager)
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           bestname[s]=txt.strip()
   return bestname
#   for s,p,o in g.triples((None,RDFS.label,None)):
#   return


def get_invs(g: rdflib.Graph) -> dict :
   """Dictionary of inverse relations (based on inverseOf and SymetricProperty"""
   inv = {}
   for s,p,o in g.triples((None,OWL.inverseOf,None)):
       inv[s]=o
       inv[o]=s
   for s,p,o in g.triples((None,RDF.type, OWL.SymmetricProperty)):
       inv[s]=s
   return inv

def get_subclass(g: rdflib.Graph) -> (dict,dict) :
   subcl = {}
   supcl = {}
   for s,p,o in g.triples((None,RDF.type,None)):
       supcl[o]=set()
   for s,p,o in g.triples((None,RDFS.subClassOf,None)):
       subcl[s]=subcl.get(s,set())
       supcl[o]=supcl.get(o,set())

       subcl[o]=subcl.get(o,set()) | {s}  ### | subcl.get(s,set())
       supcl[s]=supcl.get(s,set()) | {o} 
   subcl[OWL.Thing]=[x for x in supcl if not supcl[x]]
   return (subcl, supcl)

def pptopdown(g,top,vis,cls,indent):
    if top in vis: return
    vis[top]=1 
    print( f'{"  " * indent}{pp(g,top)}' )
    for a in sorted(cls.get(top,[]),key=termcmp):
        pptopdown(g,a,vis,cls,indent+2)

def ppsubclass(g,s,opt):
    subcl,supcl=s 
    if "-r" in opt:
       for a in sorted(supcl,key=termcmp):
          print(pp(g,a), "→",str.join("\n  ", [""]+[pp(g,x) for x in supcl[a]]))
    elif "-t" in opt:
       for a in sorted(subcl,key=termcmp):
          print(pp(g,a), "→",str.join("\n  ", [""]+[pp(g,x) for x in subcl[a]]))
    else:
       vis={}
       pptopdown(g,OWL.Thing,vis,subcl,0)

def pp(g:rdflib.Graph,term) -> str:
   """ returns a Prety printed a URIRef or Literal """
   return term.n3(g.namespace_manager)

def xpp(g:rdflib.Graph,term) -> str:
   """ returns a xdxf Prety printed URIRef """
   txt = term.n3(g.namespace_manager)
   if islit(term):
       if '"""' in txt  or "'''" in txt:
           return "<deftext>"+ sub(r'[<>&]','=',term.n3(g.namespace_manager)) + "</deftext>"
       else:
           return sub(r'[<>&]','=',term.n3(g.namespace_manager))
   else:
       txt = sub(r'^:', '', txt)
       txt = sub(r'_', ' ', txt)
       return sub(r'[<>&]','=',txt)

def simplify_class(g: rdflib.Graph, cls:list) -> list:
   """ FIXME: remove redundant class from a class list"""
   return set(cls) - {OWL.Thing, OWL.NamedIndividual}

def reduce_graph(g,fixuri=None,fixlit=None)-> rdflib.Graph:
   def fix(item):
        if islit(item) and fixlit:
            return rdflib.term.Literal(fixlit(str(item)))
        if isinstance(item, rdflib.term.URIRef) and fixuri:
            return rdflib.term.URIRef(fixuri(str(item)))
        return item

   fixed= rdflib.Graph()
   fixed.bind('owl',OWL)
   fixed.bind('rdf',RDF)
   fixed.bind('rdfs',RDFS)
   fixed.bind('skos',SKOS)
   fixed.bind('foaf',FOAF)

   fixed+= [ (fix(s), fix(p), fix(o)) for s,p,o in g]
   return fixed

def rename_label2term(files:list, opt: dict) -> rdflib.Graph :
   g = rdflib.Graph(base="http://it/")
   g.bind("",rdflib.Namespace("http://it/"))
   newname = {}
   for f in files:
      if ".n3" in f or ".ttl" in f or "-t" in opt:
         try:
             # g.parse(f,format='turtle')
             g.parse(f,format='n3')
         except Exception as e:
             warn("#### Error in ", f,e)
      else:
         try:
             g.parse(f) #,format='xml')
         except Exception as e:
             warn("#### Error in ", f,e)

   for s,p,o in g.triples((None,RDFS.label,None)):
      base = sub(r'(.*[#/]).*',r'\1',str(s))
      newid = sub(r' ','_', str(o).strip())
      newname[str(s)] = base + newid

   def rename(t):
      if str(RDF) in t or str(OWL) in t or str(RDFS) in t : 
          return t
      else: 
          return newname.get(t,t)
          return  sub(r'(http|file).*[#/]',r'http://it/',t)
   g2=reduce_graph(g, fixuri=rename)
   g2.bind("","http://it/")
   return g2

def concatload(files:list, opt: dict) -> rdflib.Graph :
   g = rdflib.Graph(base="http://it/")
   g.bind("",rdflib.Namespace("http://it/"))
   g.bind('owl',OWL)
   g.bind('rdf',RDF)
   g.bind('rdfs',RDFS)
   g.bind('skos',SKOS)
   g.bind('foaf',FOAF)
   for f in files:
      if ".n3" in f or ".ttl" in f or "-t" in opt:
         try:
             # g.parse(f,format='turtle')
             g.parse(f,format='n3')
         except Exception as e:
             warn("#### Error in ", f,e)
      else:
         try:
             g.parse(f) #,format='xml')
         except Exception as e:
             warn("#### Error in ", f,e)
   return g

def concatns(g:rdflib.Graph, opt: dict) -> rdflib.Graph :
   def fixu(t):
      if str(RDF) in t or str(OWL) in t or str(RDFS) in t : 
          return t
      else: 
          return  sub(r'(http|file).*[#/]',r'http://it/',t)

   g2=reduce_graph(g, fixuri=fixu)
   g2.bind("","http://it/")
   return g2

def concat(files:list, opt: dict) -> rdflib.Graph :
   g=concatload(files, opt)
   def fixu(t):
      if str(RDF) in t or str(OWL) in t or str(RDFS) in t : 
          return t
      else: 
          return  sub(r'(http|file).*[#/]',r'http://it/',t)

   g2=reduce_graph(g, fixuri=fixu)
   g2.bind("","http://it/")
   return g2

def off_owlbaseit(files:list):
   g = rdflib.Graph(base="http://it/")
   g.namespace_manager.bind("a",rdflib.Namespace("http://it/"))
   #g.bind("", rdflib.Namespace(pref))
   name=""
   for f in files:
      if ".ttl" in f or "-t" in c.opt:
         g.parse(f,format='turtle')
      else:
         g.parse(f) #,format='xml')
      for s,p,o in g.triples((None,RDF.type,OWL.Ontology)):
         pref = sub(r'#?$','#',s)
         ontons= rdflib.Namespace(pref)
         g.namespace_manager.bind(name,ontons,override=True,replace=True)
      print("###",len(g))
   print(g.serialize(format="turtle").decode('utf-8'))
   print("=====================================")
   g2=reduce_graph(g,
      fixlit=lambda x: sub(r'(\w)',r'QQ_\1',x),
      fixuri=lambda x: sub(r'(http.*[#/])',r'jjj:',x),
   )
   print(g2.serialize(format="turtle").decode('utf-8'))

def turtle(g: rdflib.Graph):
   serial(g,fmt="turtle")
#   print(g.serialize(format="turtle").decode('utf-8'))

def serial(g: rdflib.Graph,fmt="turtle"):
   print(g.serialize(format=fmt).decode('utf-8'))

def termcmp(t):
   return  unidecode(sub(r'.*[#/]','',t).lower())


def expand_and_print_xdxf(g: rdflib.Graph):
   owlrl.DeductiveClosure(owlrl.OWLRL_Extension_Trimming ).expand(g)
   ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
      OWL.equivalentProperty }
   instances={}
   for s,p,o in g.triples((None,RDF.type, None)):
       instances[o]=instances.get(o,[]) + [s]
   INV = get_invs(g)

   print(f"""<?xml version="1.0" encoding="UTF-8" ?>
<xdxf lang_from="POR" lang_to="DE" format="logical" revision="033">
    <meta_info>
        <title>Dicionário</title>
        <full_title>Dicionário</full_title>
        <file_ver>001</file_ver>
        <creation_date></creation_date>
    </meta_info>
<lexicon>""")

   for n in sorted(g.all_nodes(), key=termcmp):
       if islit(n): continue
       if n in [OWL.Thing] : continue
       term_inf_xdxf(g,n,instances)
   print("</lexicon>\n</xdxf>")

def islit(t):
   return isinstance(t,rdflib.term.Literal)

def term_inf_xdxf(g,n,instances):
   INV = get_invs(g)
   ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
      OWL.equivalentProperty }

   print("")
   if n in instances:
       print(f'<ar><k>{xpp(g,n)}</k><def>')
       cls = simplify_class(g, g.objects(subject=n,predicate=RDF.type))
       for c in cls:
           print( f"<kref>{xpp(g,c)}</kref>")
       for s,p,o in g.triples((n,None,None)):
           if p in ignore_pred: continue
           if islit(o):
               print( f"    <def>{xpp(g,p)}: {xpp(g,o)}</def>" )
           else:
               print( f"    <def>{xpp(g,p)}: <kref>{xpp(g,o)}</kref></def>" )
       for i in sorted(instances[n],key=termcmp):
           print( f" <def><kref>{xpp(g,i)}</kref></def>" )
       print(f'</def></ar>')
           
   else:
       print(f'<ar><k>{xpp(g,n)}</k><def>')
       cls = simplify_class(g, g.objects(subject=n,predicate=RDF.type))
       for c in cls:
           print( f"<kref>{xpp(g,c)}</kref>")
       for p,o in sorted(g.predicate_objects(n)):
           if p in ignore_pred: continue
           if islit(o):
               print( f"    <def>{xpp(g,p)}: {xpp(g,o)}</def>" )
           else:
               print( f"    <def>{xpp(g,p)}: <kref>{xpp(g,o)}</kref></def>" )
       for s,p in sorted(g.subject_predicates(n)):
           if p in ignore_pred: continue
           if p in INV: continue
           print( f"    <def><kref>{xpp(g,s)}</kref>  {xpp(g,p)} ⭕</def>" )
       print(f'</def></ar>')

def expand_and_pprint(g: rdflib.Graph):
   owlrl.DeductiveClosure(owlrl.OWLRL_Extension_Trimming ).expand(g)
   ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
      OWL.equivalentProperty }

   INV = get_invs(g)

   for n in sorted(g.all_nodes(), key=termcmp):
       if islit(n): continue
       if n in [OWL.Thing] : continue
       pterm_inf(g,n)

def pterm_inf(g,n):
   INV = get_invs(g)
   ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
      OWL.equivalentProperty }

   print("====")
   print(pp(g,n))
   cls = simplify_class(g, g.objects(subject=n,predicate=RDF.type))
   for c in cls:
       print("    ", pp(g,c))
   for s,p,o in g.triples((n,None,None)):
       if p in ignore_pred: continue
       print( "       ", pp(g,p), pp(g,o))
   for s,p,o in g.triples((None,None,n)):
       if p in ignore_pred: continue
       if p in INV: continue
       print( "       ", pp(g,s), pp(g,p), "⭕")

def grep(pat,g,opt):
   for n in sorted(g.all_nodes(), key=termcmp):
       if islit(n): continue
       if n in [OWL.Thing] : continue
       if search( pat, pp(g,n)):
           pterm_inf(g,n)

def mconcat():
   c=clfilter(opt="f:kpcto:")  
   g=concat(c.args,c.opt)
   if "-f" in c.opt:
       serial(g,fmt=c.opt["-f"])
   else:
       serial(g)

def mlabel2term():
   c=clfilter(opt="f:kpcto:")  
   g=rename_label2term(c.args,c.opt)
   g2=concatns(g,c.opt)
   if "-f" in c.opt:
       serial(g2,fmt=c.opt["-f"])
   else:
       serial(g2)

def mgrep():
   c=clfilter(opt="kpcto:")  
   pat=c.args.pop(0) 
   g=concat(c.args,c.opt)
   owlrl.DeductiveClosure(owlrl.OWLRL_Extension_Trimming ).expand(g)
   grep(pat,g,c.opt)

def mexpandpp():
   c=clfilter(opt="kpcto:")  
   g=concat(c.args,c.opt)
   expand_and_pprint(g)

def mxdxf():
   c=clfilter(opt="kpcto:")  
   g=concat(c.args,c.opt)
   expand_and_print_xdxf(g)

def mclass():
   c=clfilter(opt="rkpcto:")  
   g=concat(c.args,c.opt)
   ppsubclass(g,get_subclass(g),c.opt)

def mn32owl():
   c=clfilter(opt="f:rkpcto:")  
   g=concatload(c.args,c.opt)
   if "-f" in c.opt:
       serial(g,fmt=c.opt["-f"])
   else:
       serial(g)
