import asciianim as a
a.createcanvas(100,100,False)
obj = a.import_obj("sphere.obj")
while True:
    p = obj.p
    a.rya(0.03,p)
    a.rxa(0.03,p)
    obj.p = p
    a.Draw_Object(obj,2,True,False)
    a.draw()
    a.clearbg()

input()


    
