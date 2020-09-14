#!/usr/bin/python3

###############################################################################
# EDE:
#       Adding some extra stuff here to handle result scaling. The original
#       code sends [mm], but we want to use SI units ([m]). The scaling for
#       FC->Elmer is done by the 'writer.py' code.
#
#       Straight forward approach would be doing the reverse scaling
#       ([m]->[mm]) on-the-fly while reading the result VTU file. But this
#       code is not reachable from here (at least I could not find it).
#       As an alternative we will do the following steps:
#
#       - read Elmer result VTU
#       - scale affected data
#       - write scaled VTU file
#       - pass this one to the original code
#
#       TODO: The wasts RAM and disk space. Someone (you) should implement
#             the on-the-fly method.
#
#       Note: Python3 does use different map(). Need to convert to list !
#

import operator
import vtk 
import sys

#------------------------------------------------------------------------------
# define a class for identifing all fields to modify 
#------------------------------------------------------------------------------

class affected():
    def __init__(self,name,data):
        self.name = name                # name of field/variable
        self.data = data[:]             # modifier (scale)
        self.dlen = len( self.data )    # precalc len

    def Match(self, name, dlen ):
        if dlen != self.dlen:
            return False, []
        if name != self.name:
            return False, []
        return True, self.data

#------------------------------------------------------------------------------
# define a function doing the actual scaling 
#------------------------------------------------------------------------------

def ResultScale( ifName, ofName ):

    SCALE_M_TO_MM = 1000.0

    # put all affected fields into our wanted list ----------------------------
        
    wanted = [
        affected( 'Points',                 [ SCALE_M_TO_MM ] * 3 ),
        affected( 'PointData/displacement', [ SCALE_M_TO_MM ] * 3 ) ]

    # read input --------------------------------------------------------------

    print( 'Reading ' + ifName )
    
    reader = vtk.vtkXMLUnstructuredGridReader()         # setup reader
    reader.SetFileName( ifName )
    reader.Update()

    dataset = reader.GetOutput()                        # read the dataset

    numPoints = dataset.GetNumberOfPoints()
    numCells  = dataset.GetNumberOfCells()

    print('Number of Points: ' + str(numPoints) )       # verbose
    print('Number of Cells:  ' + str(numCells) )

    # process all points ------------------------------------------------------

    points = dataset.GetPoints()

    suspectLen  = len(points.GetPoint(0))   # assume same coords cnt for all
    suspectName = 'Points'

    for suspect in wanted:
        found,scale = suspect.Match(suspectName,suspectLen)
        if found:
            print( 'Found Points: Scaling is ' + str(scale) )
            for i in range(0,numPoints):
                points.SetPoint( i, list( map( operator.mul,
                                               points.GetPoint(i),
                                               scale ) ) )                               
                  
    # iterate all point data fields -------------------------------------------
            
    data = dataset.GetPointData()

    numArrays = data.GetNumberOfArrays()  # this is the number of data arrays

    for i in range(0, numArrays):
        array = data.GetArray(i)

        suspectLen  = array.GetNumberOfComponents()
        suspectName = 'PointData/' + array.GetName()
        found       = False
    
        for suspect in wanted:
            found,scale = suspect.Match(suspectName,suspectLen)
            if found:
                print( 'Scaling ' + suspectName + ': Scaling is ' + str(scale) )
                for i in range(0,numPoints):
                    if suspectLen == 1:
                        array.SetValue( i, GetValue(i) * scale[0] )
                    else:
                        array.SetTuple( i, list( map( operator.mul,
                                                      array.GetTuple(i),
                                                      scale ) ) ) 
                break;
        else:
            print( 'Keeping ' + suspectName )

    # write scaled output -----------------------------------------------------

    print( 'Writing ' + ofName )
    
    writer = vtk.vtkXMLUnstructuredGridWriter()     # setup writer
    writer.SetFileName( ofName )
    writer.SetInputData( dataset )

    writer.Write()                                  # write to outfile

    # done. -------------------------------------------------------------------

    print( 'Done.' )
 
#~EDE:
###############################################################################


if __name__ == '__main__':

    try:
    
        ifName = sys.argv[1]
        ofName = sys.argv[2]

        ResultScale( ifName, ofName )
          
    except:

        print( 'Something when wrong!' )
        raise                   # show whats wrong
        sys.exit( 1 )


    sys.exit( 0 )
