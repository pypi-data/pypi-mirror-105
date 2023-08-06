"""
Packing includes the ability to create basic and complex shapes.
"""


import numpy as np
from copy import deepcopy

class ElementaryShape:
    
    #################### DATA
    
    #name of elementary shape: disk, rect, triangle, ellipsoid, pyramid, tetrahedron, cone, torus
    name = ""
    
    #dimensions in metres
    dimensions = np.array([0.0, 0.0, 0.0])
    
    #shape centre coordinates position, relative to mesh
    position = np.array([0.0, 0.0, 0.0])
    
    #rotation in degrees as psi (around y), theta (around x), phi (around z)
    rotation = np.array([0.0, 0.0, 0.0])
    
    #number of x, y, z repetitions for generating arrays
    repetitions = np.array([1, 1, 1])
    
    #x, y, z displacement in metres used when generating arrays
    displacement = np.array([0.0, 0.0, 0.0])
    
    #method used to draw shape: add, sub, xor, and
    method = "add"
    
    #################### CTOR
    
    def __init__(
            self,
            name = "",
            dimensions = np.array([0.0, 0.0, 0.0]), 
            position = np.array([0.0, 0.0, 0.0]),
            rotation = np.array([0.0, 0.0, 0.0]),
            repetitions = np.array([1, 1, 1]),
            displacement = np.array([0.0, 0.0, 0.0]),
            method = "add"): 
        
        self.name = deepcopy(name)
        self.dimensions = np.array(deepcopy(dimensions))
        self.position = np.array(deepcopy(position))
        self.rotation = np.array(deepcopy(rotation))
        self.repetitions = np.array(deepcopy(repetitions))
        self.displacement = np.array(deepcopy(displacement))
        self.method = np.array(deepcopy(method))
        
    #################### DIMENSIONS
        
    def setdimensions(self, dimensions):
        """set dimensions of elementary shape"""
        self.dimensions = np.array(deepcopy(dimensions))
        
    def scale(self, scalefactors):
        """scale dimensions of elementary shape"""
        self.dimensions *= np.array(scalefactors)
            
    #################### POSITION
            
    def setposition(self, position):
        """set position of elementary shape"""
        self.position = np.array(deepcopy(position))
        
    def move(self, positionshift):
        """translate position of elementary shape"""
        self.position += np.array(positionshift)
        
    #################### ROTATION
            
    def setrotation(self, rotation):
        """set rotation of elementary shape"""
        self.rotation = np.array(deepcopy(rotation))
        
    def rotate(self, rotation):
        """rotate elementary shape"""
        self.rotation += np.array(rotation)
        
    #################### REPETITIONS
            
    def setrepetitions(self, repetitions, displacement):
        """set number of repetitions and displacement of elementary shape for generating array"""
        self.repetitions = np.array(deepcopy(repetitions))
        self.displacement = np.array(deepcopy(displacement))
        
    #################### METHOD
    
    def setaddshape(self):
        self.method = "add"
        
    def setsubshape(self):
        self.method = "sub"
        
    def is_additive(self):
        return self.method == "add"
    
    def is_subtractive(self):
        return self.method == "sub"
    
    #################### CONVERSION
    
    def tostring(self):
        lst = [self.dimensions, self.position, self.rotation, self.repetitions, self.displacement]
        text_lst = [self.name] + [" ".join(map(str, elem)) for elem in lst] + [self.method]
        return " ".join(map(str, text_lst))

###############################################################################################################################

class Shape:
    
    #################### DATA
    
    #List of elementary shapes
    shapes = []
    
    #################### CTOR
    
    def __init__(self, shape = ElementaryShape()):
        self.shapes = [deepcopy(shape)]
        
    #################### OPERATORS
        
    #Add two shapes, returning new copy
    def __add__(self, shape_right):
        
        newshape = Shape()
        newshape.shapes = deepcopy(self.shapes) + deepcopy(shape_right.shapes)
        return newshape
    
    #Subtract two shapes, returning new copy
    def __sub__(self, shape_right):
        
        newshape_left = deepcopy(self)
        newshape_right = deepcopy(shape_right)
        for shape in newshape_right.shapes:
            if shape.is_additive(): shape.setsubshape()
            elif shape.is_subtractive(): shape.setaddshape()
        return newshape_left + newshape_right
      
    #################### AUXILIARY
    
    def rotate_object_yxz(self, r, psi_theta_phi_deg):
        
        psi, theta, phi = psi_theta_phi_deg[0] * np.pi / 180, psi_theta_phi_deg[1] * np.pi / 180, psi_theta_phi_deg[2] * np.pi / 180
        rr = np.array(r)
        
        rr[0] = (np.cos(psi) * np.cos(phi) + np.sin(psi) * np.sin(theta) * np.sin(phi)) * r[0] + (np.cos(phi) * np.sin(psi) * np.sin(theta) - np.cos(psi) * np.sin(phi)) * r[1] + (np.cos(theta) * np.sin(psi)) * r[2]
        rr[1] = (np.cos(theta) * np.sin(phi)) * r[0] + (np.cos(theta) * np.cos(phi)) * r[1] - np.sin(theta) * r[2]
        rr[2] = (np.cos(psi) * np.sin(theta) * np.sin(phi) - np.cos(phi) * np.sin(psi)) * r[0] + (np.cos(psi) * np.cos(phi) * np.sin(theta) + np.sin(psi) * np.sin(phi)) * r[1] + (np.cos(psi) * np.cos(theta)) * r[2]
        return rr
    
    #################### DIMENSIONS
    
    def setdimensions(self, dimensions):
        """set dimensions of first elementary shape contained, and scale everything else in proportion"""
        scalefactors = np.array(dimensions) / self.shapes[0].dimensions
        self.scale(scalefactors)
        return self
        
    def scale(self, scalefactors):
        """scale dimensions of shape"""
        current_position = self.shapes[0].position
        for shape in self.shapes: 
            shape.scale(scalefactors)
            shape.setposition(current_position + (shape.position - current_position) * scalefactors)
        return self
    
    #################### POSITION    
    
    def setposition(self, position):
        """set position of shape, defined by the position of the first elementary shape contained"""
        current_position = self.shapes[0].position
        self.shapes[0].setposition(position)
        for shape in self.shapes[1:]: shape.move(position - current_position)
        return self
        
    def move(self, positionshift):
        """translate position of shape"""
        for shape in self.shapes: shape.move(positionshift)
        return self
        
    #################### ROTATION
    
    def setrotation(self, rotation):
        """set rotation of shape, around shape position as defined by the first elementary shape contained"""
        current_position = self.shapes[0].position
        for shape in self.shapes:
            shape.setposition(current_position + self.rotate_object_yxz(shape.position - current_position, rotation))
            shape.setrotation(rotation)
        return self
        
    def rotate(self, rotation):
        """rotate shape around shape position as defined by the first elementary shape contained"""
        current_position = self.shapes[0].position
        for shape in self.shapes:
            shape.setposition(current_position + self.rotate_object_yxz(shape.position - current_position, rotation))
            shape.rotate(rotation)
        return self
    
    #################### REPETITIONS
    
    def setrepetitions(self, repetitions, displacement):
        """set number of repetitions and displacement of shape for generating array"""
        for shape in self.shapes: shape.setrepetitions(repetitions, displacement)
        return self
        
    #################### CONVERSION
    
    def tostring(self):
        shapes_text = [shape.tostring() for shape in self.shapes]
        return " ".join(shapes_text)
        
    #################### ELEMENTARY SHAPES GENERATORS
        
    #define an elementary disk shape
    def disk(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("disk", dimensions, position))
    
    #define an elementary rectangle shape
    def rect(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("rect", dimensions, position))
    
    #define an elementary triangle shape
    def triangle(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("triangle", dimensions, position))
    
    #define an elementary ellipsoid shape
    def ellipsoid(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("ellipsoid", dimensions, position))
    
    #define an elementary pyramid shape
    def pyramid(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("pyramid", dimensions, position))
    
    #define an elementary tetrahedron shape
    def tetrahedron(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("tetrahedron", dimensions, position))
    
    #define an elementary cone shape
    def cone(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("cone", dimensions, position))
    
    #define an elementary torus shape
    def torus(dimensions = np.array([0.0, 0.0, 0.0]), position = np.array([0.0, 0.0, 0.0])):
        return Shape(ElementaryShape("torus", dimensions, position))

        
###############################################################################################################################
