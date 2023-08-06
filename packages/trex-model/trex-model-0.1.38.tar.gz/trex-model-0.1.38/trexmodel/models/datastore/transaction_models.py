'''
Created on 1 Apr 2021

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.customer_models import Customer
import trexmodel.conf as model_conf
from trexlib.utils.string_util import random_number, is_not_empty
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet,\
    MerchantUser
import logging
from trexlib.utils.common.cache_util import cache
from trexmodel import conf
from datetime import datetime,date, timedelta
from trexmodel.conf import HANDLE_DATETIME_WITH_GMT, SERVER_DATETIME_GMT

logger = logging.getLogger('model')


def generate_transaction_id(prefix=''):
    now                 = datetime.now()
    datetime_str        = now.strftime('%y%m%d%H%M%S')
    random_str_value    = random_number(6)
    
    return prefix[0:7] + datetime_str + random_str_value

class CustomerTransaction(BaseNModel, DictModel):
    '''
    
    '''
    transact_merchant            = ndb.KeyProperty(name="transact_merchant", kind=MerchantAcct)
    transact_outlet             = ndb.KeyProperty(name="transact_outlet", kind=Outlet)
    
    transact_datetime           = ndb.DateTimeProperty(required=True)
    created_datetime            = ndb.DateTimeProperty(required=True, auto_now=True)
    
    transaction_id              = ndb.StringProperty(required=True)
    invoice_id                  = ndb.StringProperty(required=False)
    remarks                     = ndb.StringProperty(required=False)
    
    tax_amount                  = ndb.FloatProperty(required=False, default=.0)
    transact_amount             = ndb.FloatProperty(required=True)
    
    
    transact_by                 = ndb.KeyProperty(name="created_by", kind=MerchantUser)
    transact_by_username        = ndb.StringProperty(required=False)
    
    entitled_reward_summary     = ndb.JsonProperty()
    entitled_voucher_summary    = ndb.JsonProperty()
    
    
    dict_properties         = ['transaction_id', 'invoice_id', 'remarks', 'tax_amount', 'transact_amount', 
                               'entitled_reward_summary', 'entitled_voucher_summary', 'transact_customer_acct', 'transact_outlet_details',
                               'transact_datetime', 'created_datetime',  'transact_outlet_key', 
                               'transact_by_username']
    
    def to_transaction_details_json(self):
        pass
    
    @property
    def transact_customer_acct(self):
        return Customer.fetch(self.key.parent().urlsafe())
    
    @property
    def transact_user_acct_key(self):
        return Customer.fetch(self.key.parent().urlsafe()).registered_user_acct_key
    
    @property
    def transact_merchant_acct(self):
        return MerchantAcct.fetch(self.transact_merchant.urlsafe())
    
    @property
    def transact_outlet_key(self):
        return self.transact_outlet.urlsafe()
    
    @property
    def transact_merchant_acct_key(self):
        return self.transact_merchant.urlsafe()
    
    @property
    def transact_customer_key(self):
        return self.key.parent().urlsafe()
    
    @property
    def transact_outlet_details(self):
        return Outlet.fetch(self.transact_outlet.urlsafe())
    
    @property
    def transact_by_user(self):
        return MerchantUser.fetch(self.transact_by.urlsafe())
    
    @staticmethod
    def create(customer, transact_amount=.0, tax_amount=.0, invoice_id=None, remarks=None, transact_outlet=None, transact_by=None, transact_datetime=None):
        
        if is_not_empty(transact_by):
            if isinstance(transact_by, MerchantUser):
                transact_by_username = transact_by.username

        
        transaction_id = generate_transaction_id()
        
        if transact_datetime is None:
            transact_datetime = datetime.now()
            if HANDLE_DATETIME_WITH_GMT:
                transact_datetime = transact_datetime - timedelta(hours=int(SERVER_DATETIME_GMT))
        
        logger.debug('generated transaction_id=%s', transaction_id)
        logger.debug('invoice_id=%s', invoice_id)
        logger.debug('tax_amount=%s', tax_amount)
        logger.debug('transact_amount=%s', transact_amount)
        logger.debug('transact_datetime=%s', transact_datetime)
        logger.debug('transact_by_username=%s', transact_by_username)
        
        customer.last_transact_datetime = transact_datetime
        
        customer_transaction = CustomerTransaction(
                                                    parent                  = customer.create_ndb_key(),
                                                    
                                                    transact_merchant       = customer.registered_merchant_acct.create_ndb_key(),
                                                    transact_outlet         = transact_outlet.create_ndb_key(),
                                                    
                                                    tax_amount              = tax_amount,
                                                    transact_amount         = transact_amount,
                                                    
                                                    transaction_id          = transaction_id,
                                                    invoice_id              = invoice_id,
                                                    remarks                 = remarks,
                                                    
                                                    transact_by             = transact_by.create_ndb_key(),
                                                    transact_by_username    = transact_by_username,
                                                    
                                                    transact_datetime       = transact_datetime,
                                                    )
        
        customer_transaction.put()
        customer.put()
        
        return customer_transaction
    
    @staticmethod
    def list_customer_transaction(customer_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key()).order(-CustomerTransaction.transact_datetime)
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def get_by_transaction_id(transaction_id):
        return CustomerTransaction.query(CustomerTransaction.transaction_id==transaction_id).get()
    
    @staticmethod
    def list_transaction_by_date(transact_date, transact_outlet=None, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        
        transact_datetime           = datetime.combine(transact_date, datetime.min.time())
        next_day_transact_datetime  = transact_datetime + timedelta(days=1)
        
        logger.debug('transact_datetime=%s',transact_datetime)
        logger.debug('next_day_transact_datetime=%s',next_day_transact_datetime)
        
        if transact_outlet:
            query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key()
                                    )).order(-CustomerTransaction.transact_datetime)
        else:
            query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    )).order(-CustomerTransaction.transact_datetime)
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_all(offset=0, limit=conf.MAX_FETCH_RECORD):
        
        query = CustomerTransaction.query()
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit)
    
    @staticmethod
    def count_customer_transaction(customer_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def count_transaction_by_date(transact_date, transact_outlet=None, limit=conf.MAX_FETCH_RECORD):
        
        transact_datetime           = datetime.combine(transact_date, datetime.min.time())
        next_day_transact_datetime  = transact_datetime + timedelta(days=1)
        
        logger.debug('transact_datetime=%s',transact_datetime)
        logger.debug('next_day_transact_datetime=%s',next_day_transact_datetime)
        
        if transact_outlet:
            query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key()
                                    ))
        else:
            query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    ))
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)
    
class CustomerTransactionWithRewardDetails(object):    
    
    def __init__(self, transaction_details, reward_details):
        self.transact_customer_key          = transaction_details.transact_customer_key
        self.transact_merchant_acct_key     = transaction_details.transact_merchant_acct_key
        self.transact_outlet_key            = transaction_details.transact_outlet_key
        self.transact_datetime              = transaction_details.transact_datetime
        self.transaction_id                 = transaction_details.transaction_id
        self.transact_amount                = transaction_details.transact_amount
        
        self.reward_format                  = reward_details.reward_format
        self.reward_amount                  = reward_details.reward_amount
        self.expiry_date                    = reward_details.expiry_date
        self.rewarded_datetime              = reward_details.rewarded_datetime
        self.reward_format_key              = reward_details.reward_format_key
        
    
    
    
    
        
      
        
        
    
        