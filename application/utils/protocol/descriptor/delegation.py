from application.utils.protocol.descriptor import AbstractDescriptor
from application.tool.enumerator.utils.design.pubsub.broker import AbstractSingletonBroker
from application.tool.enumerator.utils.design.pubsub.subscriber import AbstractSubscriber

from functools import partial

class delegate(AbstractDescriptor):
    '''
    A non-data descriptor - meant to provide a coroutine with distribution-workers, by acting as a decorator.
    '''

    def __init__(self,fget):
        '''
        Initializes a descriptor with a getter unbound method.
        :param fget:
        '''
        self.__fget=fget

    def __get__(self,instance,owner=None):
        '''
        Procedes to hand execution down to __call__ - providing an instance,
        using the partial function.
        :param instance:
        :param owner:
        :return:
        '''
        return partial(self.__call__,instance)


    def __call__(self, *args, **kwargs):
        '''
        Executes now bounded method, providing a "subscriber" key-value item, by further alteration:
        Anticipates to be provided with:
        - an instance :: AbstractSingletonBroker
        - a topic : str
        Proceeds to pack all of the data as a notification packet.
        Injects a new key-value item a "recipient" of the current push, being:
        - if there is not
        :param args:
        :param kwargs:
        :return None:
        '''
        instance, topic = (args+(None,None))[:2]
        assert instance.__class__ == AbstractSingletonBroker, TypeError('Invoker must be a broker.')
        assert isinstance(topic, str), TypeError('Topic must be a string.')

        topics=getattr(instance,f'_{instance.__class__.__name__}__topics',{})
        assert isinstance((subscribers:=topics.get(topic,None)),list), KeyError('Topic hasn\'t been registered.')

        is_callback = lambda hashmap: all(
            isinstance(hashmap.get(case[0], None), case[1]) for case in (('recipient', isinstance, AbstractSubscriber), ('notification', dict))
        )

        if is_callback(kwargs) and kwargs['recipient'] in subscribers:
            recipient = subscribers[subscribers.index(kwargs.pop('recipient'))+1]
        else:
            recipient = subscribers[0]

        return self.__fget(*args,notification=kwargs,recipient=recipient)



