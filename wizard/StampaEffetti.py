# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _

class stampa_effetti_banca(osv.osv_memory):
    _name = 'stampa.effetti.banca'
    _description ='parametri per la stampa di effetti e banca di presentazione'
    _columns = {'banca':fields.many2one('res.partner.bank', 'Banca di Presentazione', required=False),
                'dadata': fields.date('Da data distinta'),
                'adata': fields.date('A data distinta'),
                
                
                }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        result = {}
        
        parametri = self.browse(cr,uid,ids)[0]
        data1 = time.strptime(parametri.dadata, "%Y-%m-%d")
        data1 =time.strftime("%d/%m/%Y",data1)
        
        data2 = time.strptime(parametri.adata, "%Y-%m-%d")
        data2 =time.strftime("%d/%m/%Y",data2)
        #import pdb;pdb.set_trace()
        banca_name = parametri.banca.acc_number
        if not parametri.banca:
            data['form']['banca']= 0 
            banca_name = 'vuoto'
        result = {'dadata':data['form']['dadata'],'adata':data['form']['adata'], 
                  'banca':data['form']['banca'],
                  'banca_name':banca_name, 'data1':data1, 'data2':data2
                  }
        return result
    
    def _print_report(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        effetti = pool.get('effetti')
        active_ids = context and context.get('active_ids', [])
        parametri = self.browse(cr,uid,ids)[0]
        Primo = True
        return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'distintebanca',
                    'datas': data,
                    }
        
    
    def check_report(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
       
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['dadata', 'adata', 'banca'])[0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        
        data['form']['parameters'] = used_context
        
        return self._print_report(cr, uid, ids, data, context=context)
    
    
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(stampa_effetti, self).view_init(cr, uid, fields_list, context=context)

        return res
    
             
    def  default_get(self, cr, uid, fields, context=None):
        #import pdb;pdb.set_trace()
        pool = pooler.get_pool(cr.dbname)
        effetti = pool.get('effetti')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
             for ordine in effetti.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
                    DtIni = False
                    
                                    
                DtFin = False
                anr = False
                    
                ord_cliente  = False
                ord_data = False
        order_method = False             
        
        
        
        return{'dadata':DtIni, 'adata':DtFin }

stampa_effetti_banca()

class stampa_effetti(osv.osv_memory):
    _name = 'effetti.stampaII'
    _description = 'funzioni stampa ordini jasper'
    _columns = {
                'dadata': fields.date('Da data scadenza', required=True),
                'adata': fields.date('A data scadenza', required=True),
                'ord': fields.selection(  (('D', 'Ordine per Data'), ('E', 'Ordine per numero')), 'Tipo di Ordinamento'),
                'presentati':fields.boolean('Solo Effetti Presentati', required=False),
         
                }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        result = {}
        result = {'dadata':data['form']['dadata'],'adata':data['form']['adata'], 
                  'order_method':data['form']['ord']}
        return result
        

  
    def _print_report(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        effetti = pool.get('effetti')
        active_ids = context and context.get('active_ids', [])
        parametri = self.browse(cr,uid,ids)[0]
        Primo = True
        var = data['form']['ord']
        if var == 'D':
            
            if parametri.presentati:
                 return{
                    'type': 'ir.actions.report.xml',
                    'report_name': 'DistintePresentate',
                    'datas': data,
                   }
            
            else:
                return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'DistinteData',
                    'datas': data,
                   }
        else:
            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'Distinte',
                    'datas': data,
                    }
 

    def check_report(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
            
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['dadata', 'adata', 'ord'])[0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['parameters'] = used_context
        return self._print_report(cr, uid, ids, data, context=context)
  
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(stampa_effetti, self).view_init(cr, uid, fields_list, context=context)

        return res
    
             
    def  default_get(self, cr, uid, fields, context=None):
        #import pdb;pdb.set_trace()
        pool = pooler.get_pool(cr.dbname)
        effetti = pool.get('effetti')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
             for ordine in effetti.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
                    DtIni = ordine['data_scadenza']
                    
                                    
                DtFin = ordine['data_scadenza']
                anr = ordine['id']    
                    
                ord_cliente  = False
                ord_data = False
        order_method = False             
        
        return{'dadata':DtIni, 'adata':DtFin, 'ord':order_method}

    

    
stampa_effetti()  

class stampa_distinte(osv.osv_memory):
    _name = 'distinte.stampa'
    _description = 'funzioni stampa ordini jasper'
    _columns = {
                'dadata': fields.date('Da data scadenza', required=True),
                'adata': fields.date('A data scadenza', required=True),
                'ord': fields.selection(  (('D', 'Ordine per Data'), ('E', 'Ordine per numero effetto')), 'Tipo di Ordinamento'),
                'name':fields.char('Numero',size=30,required=True),
                     
    }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        result = {}
        result = {'dadata':data['form']['dadata'],'adata':data['form']['adata'], 
                  'order_method':data['form']['ord'],  'name':data['form']['name']}
        return result
        

  
    def _print_report(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        effetti = pool.get('effetti')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        var = data['form']['ord']
        if var == 'D':

            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'effetti_data',
                    'datas': data,
                   }
        else:
            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'effetti',
                    'datas': data,
                    }
 

    def check_report(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
            
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['dadata', 'adata', 'ord', 'name'])[0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['parameters'] = used_context
        return self._print_report(cr, uid, ids, data, context=context)
  
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(stampa_effetti, self).view_init(cr, uid, fields_list, context=context)

        return res
    
             
    def  default_get(self, cr, uid, fields, context=None):
        #import pdb;pdb.set_trace()
        #pool = pooler.get_pool(cr.dbname)
        effetti = self.pool.get('distinte.effetti')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
             for ordine in effetti.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
		    #import pdb;pdb.set_trace()
                    DtIni = ordine['data_distinta']
                    name = ordine['name']
                                    
                DtFin = ordine['data_distinta']
                anr = ordine['id']        
                ord_cliente  = False
                ord_data = False
                name = ordine['name']
        order_method = False             
        
        return{'dadata':DtIni, 'adata':DtFin, 'ord':order_method, 'name':name}



    
stampa_distinte() 
