import glm
vec1=glm.vec4(1, 0, 0, 2)
vec2=glm.vec4(2, 3, 4, 5)
print(vec1+vec2)

idM=glm.mat4(1.0)
amt=0.5*3.1415
rotM = glm.rotate(idM, amt, glm.vec3(0.0, 1.0, 0.0))
print(rotM)