import collections

# hashlib.sha256("test".encode()).hexdigest()

def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d:d[0])
    )
    
def pprint(chains):
    for i, chain in enumerate(chains):
        print("="*25, "Chain ", i, "="*25)
        for k, v in chain.items():
            if k == 'transactions':
                print(k)
                for d in v:
                    print("-"*40)
                    for kk, vv in d.items():
                        print(kk, vv)
            else:
                print(k, v)     
    print("*"*40)