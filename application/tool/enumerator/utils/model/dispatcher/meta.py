from application.utils.protocol.abstractmeta import AbstractMeta
from application.utils.model.requirement import NestedRequirement,TypeRequirement,MetaTypeRequirement,IterableRequirement
from application.tool.enumerator.utils.model.config import AbstractMetaConfig,MutableConfig
from abc import abstractmethod


class AbstractMetaDispatcher(AbstractMeta):

    __internal={}

    def __call__(cls, payload, length=1):
        '''
        Distributes multiple dispatchers based on a provided payload to run concurrently.
        With the help of an internal-headers hashmap , which follows a structure, denoted below:
        {
            (payload,length):tuple : MutableConfig(
                nodes:list(
                    MutableConfig(
                        wheel:StringDispatcher,
                        reset:int
                        ),
                    ...),
                ratchet:int),
            ...
        }
        The distribution itself works on top of instantiation of respective dispatchers, until it exhausts itself
        based on the provided payload and key, in following manner:

        - Requests internal header for the (payload,length) key, using the -request_header method, which creates an entry on an absent key;
            - Internally fetches multiple nodes, using the -request_node method.
        - Having retrieved a header, using the


        - Ratchets the header, using the -step method.

        - fetches a running index for the (payload,length) key from the hashmap.

        -?- If the key doesn't exist - set a default one with a value of 0
        -?> Otherwise index is assigned with an appropriate running value.

        -?- Given that the retrieved index hasn't exhausted the payload:
            - construct a dispatcher instance with the full payload,decrementing the length;
            - initialize an instance with the head as a payload , and the full length;
            - increment the index value.
        -?> Otherwise pop the distribution key out of the hashmap and apprise a StopIteration error.

        :param payload:str:
        :param length:int:
        :return:
        '''
        if not (cls.__name__ == 'StringDispatcher'): raise TypeError('The invoker must be a StringDispatcher class.')
        if not(isinstance(payload,str)): raise TypeError('Payload must be a string.')
        if not(isinstance(length,int)): raise TypeError('Length must be an integer.')

        key=(payload,length)


        cls.__request_header(payload=key[0],length=key[1])

        if (header:=cls.__step(key)) is not None:
            instance=cls.__request_wheel(
                payload=dict(
                    value=key[0],
                    length=1
                ),
                head=header,
                length=key[1]
            )
        else:
            cls.__internal.pop(key)
            raise StopIteration

        return instance

    def __request_header(cls,**key):
        '''
        Responses to requests of retrieving an internal header ,including its nodes & a respective ratchet index.
        Such action connotes:
        -?-Either simply fetching the items ,based on a provided key -> converted into a tuple(payload,length), given that such key exists
        -> Or, otherwise, creates o new entry with the following structure, requesting nodes at length-1 quantity:
            MutableConfig(
                wheel:StringDispatcher,
                reset:int
            )
            Note:In order to create a MutableConfig instance, we provide a separate dict of private attribute names and requirements.
        :param key:dict(payload:str,length:int):
        :return header-item:MutableConfig:
        '''
        if not (cls.__name__ == 'StringDispatcher'): raise TypeError('The invoker must be a StringDispatcher class.')
        if not NestedRequirement(
            payload=TypeRequirement(str),
            length=TypeRequirement(int)).validate(key) : raise ValueError('A key must contain a payload:str and a length:int.')

        key = (key['payload'], key['length'])
        return cls.__internal.setdefault(
            key,
            MutableConfig(
                {
                    'nodes':IterableRequirement(list,itemsmeta=MutableConfig),
                    'ratchet':TypeRequirement(int)
                },
                nodes=[cls.__request_node(key[0]) for _ in range(key[1])],
                ratchet=0
            )
        )

    def __request_node(cls,payload,reset=0):
        '''
        Responses to requests for an internal node - by creating a following MutableConfig:
        (
            wheel:StringDispatcher(payload,length=1) /w a head of '',
            reset:int
        )
        The latter actions are complemented , given that the invoker class is the StringDispatcher,
        payload and rest are of appropriate data types.
        :param payload:str:
        :param reset:int:
        :return node:MutableConfig:
        '''
        if not (cls.__name__ == 'StringDispatcher'): raise TypeError('The invoker must be a StringDispatcher class.')
        if not isinstance(payload,str): raise TypeError('Payload must be a string.')
        if not isinstance(reset,int): raise TypeError('Reset index must an integer.')

        return MutableConfig(
            {
                'wheel':MetaTypeRequirement(AbstractMetaDispatcher),
                'reset':TypeRequirement(int)
            },
            wheel=cls.__request_wheel(
                payload=dict(value=payload[reset:],length=1),
                head='',
                length=1
            ),
            reset=reset
        )

    def __request_wheel(cls,**data):
        '''
        Creates a wheel , which essentially is a StringDispatcher injected with data :
            - a payload:{
                value:str,
                length:int
            },
            - a head:str,
            - a length:int.
        :param data:dict:
        :return StringDispatcher as a wheel:
        '''
        if not (cls.__name__ == 'StringDispatcher'): raise TypeError('The invoker must be a StringDispatcher class.')
        if not NestedRequirement(
            payload=NestedRequirement(
                value=TypeRequirement(str),
                length=TypeRequirement(int)
            ),
            head=TypeRequirement(str),
            length=TypeRequirement(int)).validate(data) : raise ValueError('Data must contain a payload:{value:str, length:int},'
                                                                           'head:str and a length:int to create a wheel.')
        if not all(map(lambda l: l>=0 ,(data['length'],data['payload']['length']))): raise ValueError('Each length must be a non-negative int.')
        wheel = cls.__new__(cls,data['payload']['value'],data['payload']['length'])
        wheel.__init__(data['head'],data['length'])
        return wheel

    def __step(cls,key):
        '''
        Performs an action of an internal header "ratcheting", based on a provided key, and returns a string compound of the current header.
        Given that the key exists, thus a header could be retrieved, the algorithm is on to:
            -?- Verify whether a wheel of ratcheting node has been exhausted, if so:
                - Iterate through the nodes , ahead of the ratcheting one, trying to find a pusher -> index:
                    -?- If a node is clocked and still not exhausted:
                        - pusher has been found:
                            - increment the reset index of the pusher;
                            - break out of the iteration.
                    ->  Otherwise:
                        set reset index to a 0.
                -?- If the iteration hasn't been prematurely stopped,alluding that the pusher hasn't been found
                    - set pusher index to a -1;
                    - set the reset value of the current ratcheting node to a 0.
                    - increment the ratchet index -> thus delegating ratcheting to the next node.
                    -?- if the ratchet index is greater than the length of nodes:
                        - return None , inferring that the header has been fully worn out.
                    - Increment the reset value of a new ratcheting node.

                - Iterate through the nodes up to the ratcheting one, skipping the pusher:
                    - Reassign each wheel with the current payload from a key, with a respective reset index.

                - Join and return a compound of nodes, forwarding the ratcheting node and peeking at others.

        :param key:tuple(str,int):
        :return str:None:
        '''
        if not (cls.__name__ == 'StringDispatcher'): raise TypeError('The invoker must be a StringDispatcher class.')
        if not ((header:=cls.__internal.get(key,None)) is not None): raise KeyError(f'There is no internal header associated with a {key} key.')

        if header.nodes[header.ratchet].wheel.is_exhausted():

            for pusher_index in range(header.ratchet):
                if next(header.nodes[pusher_index].wheel,None) is not None and not header.nodes[pusher_index].wheel.is_exhausted():
                    header.nodes[pusher_index].reset += 1
                    break
                else:
                    header.nodes[pusher_index].reset = 0
            else:
                pusher_index = -1
                header.nodes[header.ratchet].reset = 0
                header.ratchet += 1
                if header.ratchet>len(header.nodes):
                    return None
                header.nodes[header.ratchet].reset += 1

            for index in filter(lambda i: i.__ne__(pusher_index),range(header.ratchet+1)):
                header.nodes[index].wheel=cls.__request_wheel(
                    payload=dict(value=key[0][header.nodes[index].reset:],length=1),
                    head='',
                    length=1
                )
        return ''.join( (next(node.wheel) if index==header.ratchet else node.wheel.peek())[0] for index,node in enumerate(header.nodes))











    @abstractmethod
    async def dispatch(self,hook,callback):
        raise NotImplementedError()

    @abstractmethod
    async def peek(self):
        raise NotImplementedError()

    @abstractmethod
    def is_exhausted(self):
        raise NotImplementedError()