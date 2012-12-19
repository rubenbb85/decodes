import math
import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.solarGeom as sg
import fieldpack.extensions.parseEPW as epw

def main():
  """a simple example of calculating solar incident radiation.  
  given a user-defined plane to evaluate, a hard-coded position, 
  and a EPW file that associates date/time with radiation level, 
  calculates the amount of radition striking the plane
  and produces a simple visualization.
  """
  outie = fp.makeOut(fp.outies.Rhino, "solar incidence")
  outie.set_color(Color(0.75))
  
  # getting user input
  pathPrefix = ""
  path = pathPrefix + "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
  epwdata = epwData(path)
  innie = fp.makeIn(fp.innies.Rhino)
  mymesh = innie.get_mesh()
  
  # find the normals for each mesh face
  normals = [Ray(mymesh.face_centroid(i),mymesh.face_normal(i)) for i in range(len(mymesh.faces))]
  meshNormal = [(mymesh.face_normal(i)) for i in range(len(mymesh.faces))]
  meshCentroid = [(mymesh.face_centroid(i)) for i in range(len(mymesh.faces))]
  #meshVerts = [(mymesh.face_verts(i)) for i in range(len(mymesh.faces))]
  #print meshVerts
  
  
  for normal in meshNormal:
    #midPt = []
    for centroid in meshCentroid:
      #midPt.append(centroid + normal)
      p0 = centroid + normal
  print p0
  
  #for i in range(len(mymesh.faces)):
    #meshCentroid = mymesh.face_centroid(i)
    #for i in range(len(mymesh.faces)):
      #meshNormal = mymesh.face_normal(i)
  #p0 = meshCentroid + meshNormal
  
  for i in range(len(mymesh.faces)):
    meshVerts = mymesh.face_verts(i)
  meshPts = meshVerts[:]
  #print meshPts
  meshPts[0:0] = [p0]
  #print meshPts
  
  m1 = [meshPts[0], meshPts[1], meshPts[2]]
  m2 = [meshPts[0], meshPts[2], meshPts[3]]
  m3 = [meshPts[0], meshPts[3], meshPts[4]]
  m4 = [meshPts[0], meshPts[1], meshPts[4]]
  
  meshModule = [(Mesh(m1,(0,1,2))), (Mesh(m2,(0,2,3))), (Mesh(m3,(0,3,4))), (Mesh(m4,(0,1,4)))]
  print meshModule
  
  #for n in meshCentroid:
    #print n
    #for i in range(len(mymesh.faces)):
      #meshVerts = mymesh.face_verts(i)
      #for vert in meshVerts:
        #pLine = Line(vert, n)
        #print vert
        #pirLine = Line(vert, n)
        #print pLine
    #p1 = Point(normals)
    #print p1
  
  #####Rhinoscript
  #mesh = rs.GetObject('Select Mesh')
  #verts, norms, centroid = rs.MeshVertices(mesh), rs.MeshFaceNormals(mesh), rs.MeshFaceCenters(mesh)
  #print norms
  #for norm in norms:
  #for v in verts:
    #for c in norms:
      #rs.AddLine(v, c)
  
  # setup our visualization
  colorA = Color.HSB(0.75) #saturation and brightness of HSB colors default to 1.0
  colorB = Color.HSB(0.0) #saturation and brightness of HSB colors default to 1.0
  
  # Calculate the Yearly Average or Yearly Maximum Incident Radiation
  # and Visualize Results
  for normal in normals:
    irrArr = []
    for h in range(48): irrArr.append(srfIrradiance(normal,h,epwdata))
    avgIrr = (sum(irrArr))/(len(irrArr)) #Calculates Yearly Average Radiation
    print '{} Yearly Average Radiation w/m2'.format(avgIrr)

    #visualize results
    normalizedVal = avgIrr/1000 #sets a range of 0w/m2 -> 1000w/m2
    color = Color.interpolate(colorA,colorB,normalizedVal)
    normal.set_color(color)
    normal.vec.length = normalizedVal * 10
    
  outie.put([normals, p0, ])
  outie.draw()

def epwData(filepath):
  """given a path to an EPW file, 
  extracts the direct normal irradiance, lat, long, tmz
  out: a dictionary with the above information
  """
  radValues = epw.parse_epw_file(filepath, "DirNormIrad")
  metadata = epw.epw_metadata(filepath)
  dict = {}
  dict['lat'] = metadata['lat']
  dict['long'] = metadata['long']
  dict['timezone'] = metadata['timezone']
  dict['name'] = metadata['name']
  dict['radiation'] = radValues
  return dict

def srfIrradiance(plane,hourOfYr,epwdata):
  """calculates irradiance striking a given plane at a given hour for a given location
  plane (fp.Ray) the plane in question
  hour (int) the hour of the year to test, 0-8760
  epwdata (dict) a dictionary of epw data
  out: the amount of radition striking the plane
  """
  #calculate the solar vector
  day = int(hourOfYr/24)
  hour = hourOfYr%24
  sunvec = sg.calc_sunVector(epwdata['lat'], epwdata['long'], epwdata['timezone'], day, hour)
  
  #find the angle between our plane and the sun direction
  incidenceAngle = abs(sunvec.angle(plane.vec))
  if incidenceAngle > math.pi/2 : srfIrr = 0.0 #if the sun is behind our plane, return zero
  else : srfIrr = epwdata['radiation'][hourOfYr] * math.cos(incidenceAngle) # otherwise, calculate the amout of radition striking our surface
  #print srfIrr
  return srfIrr

# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()

