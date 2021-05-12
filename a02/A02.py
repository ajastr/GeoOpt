"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""
        
import Rhino.Geometry as rg

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a


mesh = m
vec = s

faceNormals = mesh.FaceNormals.ComputeFaceNormals()

a = mesh.FaceNormals

#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

centers = []
for faceInd in range(len(mesh.Faces)):
    centers.append(mesh.Faces.GetFaceCenter(faceInd))
b = centers

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angleList = []
for i in range(len(centers)):
    angleList.append(rg.Vector3d.VectorAngle(vec,a[i]))

c = angleList


#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d
exploded = []
explodedV01 = []
duplicated = mesh.Duplicate()



for faceInd in range(len(duplicated.Faces)):
    #dupFace = duplicated.Faces[faceInd]
    #print(dupFace)
    exploded.append(duplicated.Faces.ExtractFaces([0]))

    #exploded.append(dupFace)
    
d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

newPts = []

for n in range(len(exploded)):


    centerOff =(c[n])*1.5/ 3.14
    #centerOff = centerOff ** 3
    newMesh = exploded[n]
    newVert = []

    pt1 = exploded[n].Faces.GetFaceVertices(0)[1]
    v1 = rg.Vector3d(centers[n]) - rg.Vector3d(pt1)
    newPt1 = centers[n] - v1.Multiply(v1, centerOff)
    

    pt2 = exploded[n].Faces.GetFaceVertices(0)[2]
    v2 = rg.Vector3d(centers[n]) - rg.Vector3d(pt2)
    newPt2 = centers[n] - v2.Multiply(v2, centerOff)
    newPts.append(pt2)

    newMesh.Vertices.Add(newPt1)
    newMesh.Vertices.Add(newPt2)
    newMesh.Faces.AddFace(2,3,4,5)

    pt3 = exploded[n].Faces.GetFaceVertices(0)[3]
    v3 = rg.Vector3d(centers[n]) - rg.Vector3d(pt3)
    newPt3 = centers[n] - v1.Multiply(v3, centerOff)


    pt4 = exploded[n].Faces.GetFaceVertices(0)[4]
    v4 = rg.Vector3d(centers[n]) - rg.Vector3d(pt4)
    newPt4 = centers[n] - v2.Multiply(v4, centerOff)
    #newPts.append(newPt4)

    newMesh.Vertices.Add(newPt3)
    newMesh.Vertices.Add(newPt4)
    newMesh.Faces.AddFace(1,0,6,7)

    newMesh.Faces.AddFace(4,7,1,3)
    newMesh.Faces.AddFace(0,6,5,2)

    newMesh.Faces.AddFace(4,5,6,7)
    newMesh.Faces.RemoveAt(0)
    newMesh.Faces.RemoveAt(4)


    cleanmesh = newMesh
    #methods to clean a mesh
    cleanmesh.Normals.ComputeNormals()
    cleanmesh.Vertices.CombineIdentical(True, True)
    cleanmesh.Vertices.CullUnused()
    cleanmesh.Weld(3.14159265358979)
    cleanmesh.UnifyNormals()
    cleanmesh.FaceNormals.ComputeFaceNormals()
    cleanmesh.Compact()


e = cleanmesh


#Geometry with breps
panels = []

for i in range(len(exploded)):

    sc= 0.1
    vecOffBelow = a[i].Multiply(sc, a[i])
    vecOffAbove = a[i].Multiply(-sc, a[i])

    
    j = exploded[i].Vertices

    line1 = rg.Line(j[0],j[2])
    line2 = rg.Line(j[1],j[3])

    crv1 = line1.ToNurbsCurve()
    divParams1 = crv1.DivideByCount(5,True)
    divPoints1= []
    for k in divParams1:
        divPoints1.append(crv1.PointAt(k))

    crv2 = line2.ToNurbsCurve()
    divParams2 = crv2.DivideByCount(5,True)
    divPoints2= []
    for k in divParams2:
        divPoints2.append(crv2.PointAt(k))

    
    for l in range(1,5):

        ln = rg.Line(divPoints1[l],divPoints2[l])
        

        lnBelow = rg.Line(divPoints1[l]+vecOffBelow,divPoints2[l]+vecOffBelow)
        lnAbove = rg.Line(divPoints1[l]+vecOffAbove,divPoints2[l]+vecOffAbove)
        loftCrvs = [lnBelow.ToNurbsCurve(), lnAbove.ToNurbsCurve()]
        axis = rg.Vector3d(divPoints1[l]) - rg.Vector3d(divPoints2[l]) 

        panel = rg.Brep.CreateFromLoft(loftCrvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Tight, False)[0]
        panel.Rotate(c[i],axis,ln.PointAt(0.5))
    
     
        panels.append(panel)

f = panels

