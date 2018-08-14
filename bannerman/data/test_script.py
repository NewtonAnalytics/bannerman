import sys
import bannerman.data as data

args = sys.argv[1:]
rally=data.connect_to_rally(sys.argv[1:])
