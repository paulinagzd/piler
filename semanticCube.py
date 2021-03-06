ERROR_MESSAGE = 'TYPE MISMATCH'

# This variable is the main dictionary for binary operations
# it is accessed through an operator, then their respective
# left and right values from the operation. It should return
# either the type that should be return or an error message.
SemanticCube = {
  '+': {
    'int': {
      'int': 'int',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'flt',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '-': {
    'int': {
      'int': 'int',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'flt',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '*': {
    'int': {
      'int': 'int',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'flt',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '/': {
    'int': {
      'int': 'flt',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'flt',
      'flt': 'flt',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },  
  '>': {
    'int': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '<': {
    'int': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '>=': {
    'int': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '<=': {
    'int': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': 'boo',
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
  },
  '==': {
    'int': {
      'int': 'boo',
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': ERROR_MESSAGE,
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': 'boo',
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': 'boo', 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': 'boo',
    }, 
  },
  '!=': {
    'int': {
      'int': 'boo',
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': ERROR_MESSAGE,
      'flt': 'boo',
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': 'boo',
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': 'boo', 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': 'boo',
    }, 
  },
  '&&': {
    'int': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': 'boo',
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
  },
  '||': {
    'int': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    }, 
    'flt': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'boo': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': 'boo',
      'str': ERROR_MESSAGE,
    },
    'cha': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
    'str': {
      'int': ERROR_MESSAGE,
      'flt': ERROR_MESSAGE,
      'cha': ERROR_MESSAGE, 
      'boo': ERROR_MESSAGE,
      'str': ERROR_MESSAGE,
    },
  },
}
