from itertools import chain, combinations
import queue
import pprint

class FDStorage:
    """ Computes the closure of all possible sets of attributes, given a relation and its decomposed and non-trivial functional dependencies.

    Briefly, the closure of a set of attributes can be determined by all the other attributes (including themselves) that can be "switched on",
    given the conditions imposed by the functional dependencies.

    For example,
        if A->B, the closure of A would be {A,B}. 
        if A->B; A->C; B,C->D, the closure of A would be {A,B,C,D}

    """
    def __init__(self):
        self.relation_dict = {}
        self.powerset = []
        self.attributes = []

        self.closures = {}

    def set_values(self):
        attr = input("Input relation attributes in the form 'A,B,C': ")
        fds = input("Input decomposed and non-trivial functional dependencies in the form 'A->B;A,B->C': ")
        
        relation_list = [x.strip() for x in attr.split(",")]
        fd_list = [x.strip() for x in fds.split(";")]
        
        for i in relation_list:
            self.relation_dict[i] = []
            self.attributes.append(i)

        for fd in fd_list:
            LHS, RHS = fd.split("->")
            self.relation_dict[RHS].append(LHS.split(","))

        # generate all combinations from the given attributes
        self.powerset = list(chain.from_iterable(combinations(relation_list,r) \
                                                 for r in range(1, len(relation_list)+1)))

    def _get_on_state(self, nodes:list, on_dict:dict):
        """
        Determines if all nodes in a list are switched on.

        If on_dict has the value {'A': True, 'B': True, 'C': False},
            then ['A','B'] will return True and ['A', 'C'] will return False.
        """
        return all((lambda x: on_dict[x])(node) for node in nodes)

    def _get_closure(self, s):
        """
        Returns the closure of a given set of attributes, s.
        """
        # INITIALISE VALUES
        ## switch on nodes that are provided by the set s
        on_dict = dict.fromkeys(self.attributes, False)
        for attr in s:
            on_dict[attr] = True

        ## initialise queue with all attributes in the relation
        attr_queue = queue.Queue()
        for attribute in self.attributes:
            attr_queue.put(attribute)

        # While attribute queue is not empty, search for attributes that can be "switched on"
        while not attr_queue.empty():
            attribute = attr_queue.get()
            if not on_dict[attribute]:
                if any(self._get_on_state(nodes, on_dict) for nodes in self.relation_dict[attribute]):
                    on_dict[attribute] = True
                    for key, value in self.relation_dict.items():
                        if any(attribute in sublist for sublist in value):
                            attr_queue.put(key)
        
        return list(map(lambda x: x[0], filter(lambda x: x[1], on_dict.items())))

    def compute_closures(self):
        for s in self.powerset:
            self.closures["".join(s)] = self._get_closure(s)

    def get_closures(self):
        if not self.closures:
            print("Closures dictionary currently empty. Run compute_closures first")
            
        rv = {}
        for key, value in self.closures.items():
            rv[key] = "".join(value)
        return rv

    def _get_superkeys(self):
        return map(lambda x: x[0], filter(lambda x: len(x[1]) == len(self.attributes), self.closures.items()))

    def get_superkeys(self):
        return "Superkeys: " + "; ".join(self._get_superkeys())

    def get_keys(self):
        return "Keys: " + "; ".join(filter(lambda x: len(x) == min(map(len, self._get_superkeys())), self._get_superkeys()))

# Usage
stor = FDStorage()
stor.set_values()
stor.compute_closures()
pprint.pprint(stor.get_closures())

# e.g.
# A,B,C,D
# A->C;B,C->D;C,D->A;D->B
