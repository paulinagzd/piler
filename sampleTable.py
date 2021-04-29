sampleTable = {
  "global": {
    "tipo": 'global',
    "scopeVariables": { # 0 vars
      "var1": {
        "tipo": 'int',
        "valor": 'val',
      },
    },
    "scopeFunctions": { # 1 funcs
      "func1": {
        "tipo": 'tipo',
        "scopeVariables": {
          "varParam1": {
            "tipo": 'int',
            "valor": 'val',
          },
          "varParam2": {
            "tipo": 'int',
            "valor": 'val',
          },
        },
      },
      "func2": {
        "tipo": 'tipo',
        "scopeVariables": {
          "varsParams": {
            "varParam3": {
              "tipo": 'int',
              "valor": 'val',
            },
            "varParam4": {
              "tipo": 'int',
              "valor": 'val',
            },
          },
        },
      },
    },
    "scopeClasses": { # 2 classes (if global)
      "className": { #scope redux or local
        "scopeVariables": { # 0 vars
          "varClass": {
            "tipo": 'int',
            "valor": 'val',
          },
          "varClass2": {
            "tipo": 'int',
            "valor": 'val',
          },
        },
        "scopeFunctions": { # 1 funcs
          "classFunc": {
            "tipo": 'tipo',
            "classVarsParams": {
              "classVarParam1": {
                "tipo": 'int',
                "valor": 'val',
              },
              "classVarParam2": {
                "tipo": 'int',
                "valor": 'val',
              },
            },
          },
        },
      }
    },
  }
}
