from time import gmtime, strftime
import os
import Output
finalString = strftime("%Y-%m-%d %H:%M:%S", gmtime())

outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.xlsx'

print outputPath

lista = [1, 2, 3,
          4, 5, 6]
print lista[1][2]