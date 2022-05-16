import subprocess
import time


TEMPLATE = """
--------------------- MoorDyn Input File -------------------------------------------------------
Trying to simulate a single chain swinging in seawater. Outputs should be p,t so that we 
can get the position and tension for the line!
----------------------- LINE TYPES --------------------------------------------------------------
TypeName   Diam    Mass/m     EA         BA/-zeta    EI         Cd     Ca     CdAx    CaAx
(name)     (m)     (kg/m)     (N)        (N-s/-)     (N-m^2)    (-)    (-)    (-)     (-)
chain       8.0E-3  1.1        7.51E6     -.5        0        2.4    1.0      0.1     0.0
---------------------------- BODIES --------------------------------------------------------------
ID   Attachment  X0     Y0    Z0     r0      p0     y0     Mass  CG*   I*      Volume   CdA*   Ca
(#)     (-)      (m)    (m)   (m)   (deg)   (deg)  (deg)   (kg)  (m)  (kg-m^2)  (m^3)   (m^2)  (-)
BODY_INPUT_HERE
----------------------- POINTS -------------------------------------------------------------------
Node      Type      X        Y         Z        M        V         CdA   CA
(-)       (-)      (m)      (m)       (m)      (kg)     (m^3)     (m^2)  (-)
POINT_INPUT_HERE
-------------------------- LINES -----------------------------------------------------------------
Line     LineType NodeA     NodeB  UnstrLen  NumSegs     Flags/Outputs
(-)      (-)       (-)       (-)   (m)         (-)          (-)
LINE_INPUT_HERE
-------------------------- SOLVER OPTIONS----------------------------------------------------------
2        writeLog     - Write a log file
0.0001   dtM          - time step to use in mooring integration
3.0e6    kb           - bottom stiffness
3.0e5    cb           - bottom damping
400       WtrDpth      - water depth
3.0      ICDfac       - factor by which to scale drag coefficients during dynamic relaxation IC gen
0.015    threshIC     - threshold for IC convergence
100.0    TmaxIC       - threshold for IC convergence
0.01     dtIC         - Time lapse between convergence tests (s)
------------------------- need this line -------------------------------------- 
"""

def save_specifications(spec, name):
    f = open(name, "w")
    f.write(spec)
    f.close()

def generate_template(n):
    """
    Parameters
    ----------
    n : number of MoorDyn Lines to Simulate

    Returns
    -------
    Dict formatted into the type of MoorDyn:
        {i: Bodyi_Text}
    """
    
    def make_bodyi(i):
        return "{} free 0 0 0 0 0 0 0 0 1e10 0 0 0".format(2*i)
    
    def make_pointi(i):
        return """{} Fixed 10 {} 20 0 0 0 0\n{} Body1 15 {} 16.9518 0 0 0 0""".format(2*i, 5*i, 2*i+1,  5*i)
    
    def make_linei(i):
        return "{} chain {}  {}  10  30  p".format(2*i, 2*i, 2*i-1)
    
    def insert_bodyi(i, template):
        return (make_bodyi(i) + "\nBODY_INPUT_HERE").join(template.split("BODY_INPUT_HERE"))
    
    def insert_pointi(i, template):
        return (make_pointi(i) + "\nPOINT_INPUT_HERE").join(template.split("POINT_INPUT_HERE"))
    
    def insert_linei(i, template):
        return (make_linei(i) + "\nLINE_INPUT_HERE").join(template.split("LINE_INPUT_HERE"))
    
    template = TEMPLATE
    template = insert_bodyi(1, template)
    
    for i in range(1, n-1):
        template = insert_pointi(i, template)
        template = insert_linei(i, template)
    
    template = template.replace("\nBODY_INPUT_HERE", "")
    template = template.replace("\nLINE_INPUT_HERE", "")
    template = template.replace("\nPOINT_INPUT_HERE", "")
    
    save_specifications(template, "speed_study/line_{}.txt".format(n))
    
i = 33
generate_template(i)

start = time.time()
subprocess.call(["bash", 
                 "run.sh", 
                 "/home/oliver/Desktop/kelson/MoorDyn-dev/kelson_test/speed_study/line_{}.txt".format(i)])
runtime = time.time() - start
    
    
    
    

    