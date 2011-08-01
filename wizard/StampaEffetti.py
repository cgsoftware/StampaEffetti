# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _



class stampa_effetti(osv.osv_memory):
    _name = 'effetti.stampaII'
    _description = 'funzioni stampa ordini jasper'
    _columns = {
                'dadata': fields.date('Da data scadenza', required=True),
                'adata': fields.date('A data scadenza', required=True),
                'ord': fields.selection(  (('D', 'Ordine per Data'), ('E', 'Ordine per numero effetto')), 'Tipo di Ordinamento')     
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
        Primo = True
        var = data['form']['ord']
        if var == 'D':

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
                    NrIni = ordine['name']
                                    
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
                'ord': fields.selection(  (('D', 'Ordine per Data'), ('E', 'Ordine per numero effetto')), 'Tipo di Ordinamento')     
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
        Primo = True
        var = data['form']['ord']
        if var == 'D':

            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'EffettiData',
                    'datas': data,
                   }
        else:
            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'Effetti',
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
                    NrIni = ordine['name']
                                    
                DtFin = ordine['data_scadenza']
                anr = ordine['id']        
                ord_cliente  = False
                ord_data = False
        order_method = False             
        
        return{'dadata':DtIni, 'adata':DtFin, 'ord':order_method}

    

    
stampa_distinte() 